package com.powerguard.routes

import com.powerguard.models.*
import com.powerguard.storage.ReportRepository
import io.ktor.http.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.configureApiRoutes(repository: ReportRepository) {
    route("/api") {
        // Health check & system metadata
        get("/health") {
            call.respond(
                mapOf(
                    "status" to "UP",
                    "service" to "PowerGuard Electricity Theft & Vigilance Portal",
                    "runtime" to "Kotlin ${KotlinVersion.CURRENT} / Ktor Server",
                    "database" to "SQLite Local Persistence (data/powerguard.db)",
                    "roles" to "CITIZEN, OFFICER, ADMIN"
                )
            )
        }

        // Authentication Routes (Citizen, Officer, Admin Login & Citizen Registration)
        route("/auth") {
            post("/login") {
                val req = runCatching { call.receive<LoginRequest>() }.getOrElse { err ->
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ApiResponse<AuthResponse>(success = false, message = "Invalid login payload: ${err.message}")
                    )
                    return@post
                }

                val authResult = repository.authenticate(req)
                if (authResult == null) {
                    call.respond(
                        HttpStatusCode.Unauthorized,
                        ApiResponse<AuthResponse>(
                            success = false,
                            message = "Invalid username, password, or role selection. Please check your credentials."
                        )
                    )
                } else {
                    call.respond(
                        ApiResponse(
                            success = true,
                            message = "Signed in as ${authResult.user.fullName}",
                            data = authResult
                        )
                    )
                }
            }

            post("/register") {
                val req = runCatching { call.receive<RegisterCitizenRequest>() }.getOrElse { err ->
                    call.respond(
                        HttpStatusCode.BadRequest,
                        ApiResponse<AuthResponse>(success = false, message = "Invalid registration payload: ${err.message}")
                    )
                    return@post
                }

                val result = repository.registerCitizen(req)
                result.fold(
                    onSuccess = { auth ->
                        call.respond(
                            HttpStatusCode.Created,
                            ApiResponse(
                                success = true,
                                message = "Account registered successfully! Welcome, ${auth.user.fullName}.",
                                data = auth
                            )
                        )
                    },
                    onFailure = { err ->
                        call.respond(
                            HttpStatusCode.BadRequest,
                            ApiResponse<AuthResponse>(success = false, message = err.message ?: "Registration failed")
                        )
                    }
                )
            }
        }

        // Dashboard statistics & analytics
        get("/stats") {
            val stats = repository.getDashboardStats()
            call.respond(ApiResponse(success = true, message = "Dashboard statistics retrieved", data = stats))
        }

        // Vigilance officers directory
        get("/officers") {
            call.respond(ApiResponse(success = true, message = "Vigilance officers retrieved", data = repository.officers))
        }

        // Public complaint tracking by Reference ID
        get("/reports/track/{referenceId}") {
            val refId = call.parameters["referenceId"]?.trim() ?: ""
            if (refId.isBlank()) {
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<PublicTrackingResponse>(success = false, message = "Reference ID is required.")
                )
                return@get
            }

            val report = repository.getReportByReferenceId(refId)
            if (report == null) {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<PublicTrackingResponse>(
                        success = false,
                        message = "No complaint found with Reference ID '$refId'."
                    )
                )
                return@get
            }

            val publicResponse = PublicTrackingResponse(
                referenceId = report.referenceId,
                title = report.title,
                category = report.category,
                categoryDisplay = report.category.displayName,
                severity = report.severity,
                status = report.status,
                statusDisplay = report.status.displayName,
                address = report.address,
                landmark = report.landmark.ifBlank { report.address },
                assignedOfficer = report.assignedOfficer ?: "Pending Assignment",
                inspectionNotes = report.inspectionNotes ?: "Report registered and awaiting officer assignment.",
                createdAt = report.createdAt,
                updatedAt = report.updatedAt,
                history = report.history
            )

            call.respond(
                ApiResponse(
                    success = true,
                    message = "Tracking details found for ${report.referenceId}",
                    data = publicResponse
                )
            )
        }

        // List reports
        get("/reports") {
            val status = call.request.queryParameters["status"]
            val category = call.request.queryParameters["category"]
            val severity = call.request.queryParameters["severity"]
            val search = call.request.queryParameters["search"]
            val assignedOfficerUsername = call.request.queryParameters["assignedOfficerUsername"]
            val submittedByUsername = call.request.queryParameters["submittedByUsername"]

            val reports = repository.getAllReports(
                status = status,
                category = category,
                severity = severity,
                search = search,
                assignedOfficerUsername = assignedOfficerUsername,
                submittedByUsername = submittedByUsername
            )
            call.respond(
                ApiResponse(
                    success = true,
                    message = "Retrieved ${reports.size} reports",
                    data = reports
                )
            )
        }

        // Get full details for a single report
        get("/reports/{referenceId}") {
            val refId = call.parameters["referenceId"] ?: ""
            val report = repository.getReportByReferenceId(refId)
            if (report == null) {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<TheftReport>(success = false, message = "Report '$refId' not found")
                )
            } else {
                call.respond(ApiResponse(success = true, message = "Report details retrieved", data = report))
            }
        }

        // CITIZEN ACTION: Submit a new electricity theft report
        post("/reports") {
            val req = runCatching { call.receive<CreateReportRequest>() }.getOrElse { err ->
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Invalid request payload: ${err.message}")
                )
                return@post
            }

            if (req.title.isBlank() || req.address.isBlank() || req.description.isBlank()) {
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(
                        success = false,
                        message = "Title, incident address, and detailed description are required."
                    )
                )
                return@post
            }

            val created = repository.createReport(req)
            call.respond(
                HttpStatusCode.Created,
                ApiResponse(
                    success = true,
                    message = "Electricity theft report submitted! Reference ID: ${created.referenceId}",
                    data = created
                )
            )
        }

        // ADMIN ACTION: Assign a report to a Vigilance Officer
        patch("/reports/{referenceId}/assign") {
            val refId = call.parameters["referenceId"] ?: ""
            val req = runCatching { call.receive<AdminAssignOfficerRequest>() }.getOrElse { err ->
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Invalid officer assignment payload: ${err.message}")
                )
                return@patch
            }

            if (req.assignedOfficer.isBlank()) {
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Please select a Vigilance Officer to assign.")
                )
                return@patch
            }

            val updated = repository.assignOfficerByAdmin(refId, req)
            if (updated == null) {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<TheftReport>(success = false, message = "Report '$refId' not found")
                )
            } else {
                call.respond(
                    ApiResponse(
                        success = true,
                        message = "Report ${updated.referenceId} assigned to ${updated.assignedOfficer}.",
                        data = updated
                    )
                )
            }
        }

        // OFFICER ACTION: Investigate an assigned report and update status/findings
        patch("/reports/{referenceId}/investigate") {
            val refId = call.parameters["referenceId"] ?: ""
            val req = runCatching { call.receive<OfficerInvestigationRequest>() }.getOrElse { err ->
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Invalid investigation payload: ${err.message}")
                )
                return@patch
            }

            if (req.inspectionNotes.isBlank()) {
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Please enter field inspection notes/findings.")
                )
                return@patch
            }

            val updated = repository.investigateReportByOfficer(refId, req)
            if (updated == null) {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<TheftReport>(success = false, message = "Report '$refId' not found")
                )
            } else {
                call.respond(
                    ApiResponse(
                        success = true,
                        message = "Investigation updated for ${updated.referenceId} (${updated.status.displayName})",
                        data = updated
                    )
                )
            }
        }

        // General status update endpoint
        patch("/reports/{referenceId}/status") {
            val refId = call.parameters["referenceId"] ?: ""
            val req = runCatching { call.receive<UpdateReportStatusRequest>() }.getOrElse { err ->
                call.respond(
                    HttpStatusCode.BadRequest,
                    ApiResponse<TheftReport>(success = false, message = "Invalid status update payload: ${err.message}")
                )
                return@patch
            }

            val updated = repository.updateReportStatus(refId, req)
            if (updated == null) {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<TheftReport>(success = false, message = "Report '$refId' not found")
                )
            } else {
                call.respond(
                    ApiResponse(
                        success = true,
                        message = "Case ${updated.referenceId} updated to '${updated.status.displayName}'",
                        data = updated
                    )
                )
            }
        }

        // Delete a report
        delete("/reports/{referenceId}") {
            val refId = call.parameters["referenceId"] ?: ""
            val deleted = repository.deleteReport(refId)
            if (deleted) {
                call.respond(
                    ApiResponse<String>(
                        success = true,
                        message = "Report $refId deleted successfully",
                        data = refId
                    )
                )
            } else {
                call.respond(
                    HttpStatusCode.NotFound,
                    ApiResponse<String>(success = false, message = "Report '$refId' not found")
                )
            }
        }
    }
}
