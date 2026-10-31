package com.powerguard.storage

import com.powerguard.models.*
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory
import java.io.File
import java.sql.Connection
import java.sql.DriverManager
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.UUID
import kotlin.random.Random

class ReportRepository(private val dataDir: File = File("data")) {
    private val logger = LoggerFactory.getLogger(ReportRepository::class.java)
    private val json = Json {
        prettyPrint = true
        ignoreUnknownKeys = true
        encodeDefaults = true
    }
    private val dbFile = File(dataDir, "powerguard.db")
    private val jsonMirrorFile = File(dataDir, "reports_mirror.json")
    private val dbHtmlFile = File(dataDir, "view_database.html")
    private val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")

    val officers: List<VigilanceOfficer> = listOf(
        VigilanceOfficer("OFF-101", "officer1", "Er. Vikramaditya Deshmukh", "VIG-EI-09", "Chief Grid Inspector", "+91 98110-44203"),
        VigilanceOfficer("OFF-102", "officer2", "Er. Priya Nair", "VIG-CC-01", "Assistant Enforcement Officer", "+91 98110-44202"),
        VigilanceOfficer("OFF-103", "officer3", "Er. Rajesh Sharma", "VIG-NZ-04", "Senior Vigilance Engineer", "+91 98110-44201"),
        VigilanceOfficer("OFF-104", "officer4", "Er. Ananya Verma", "VIG-SR-12", "Field Vigilance Inspector", "+91 98110-44204"),
        VigilanceOfficer("OFF-105", "officer5", "Er. Mohammed Farooq", "VIG-WR-07", "Line Vigilance Supervisor", "+91 98110-44205")
    )

    init {
        if (!dataDir.exists()) {
            dataDir.mkdirs()
        }
        initDatabase()
        seedUsersIfNeeded()
        logger.info("Initialized SQLite database at ${dbFile.absolutePath} with ${getAllReports().size} reports.")
    }

    private fun getConnection(): Connection {
        return DriverManager.getConnection("jdbc:sqlite:${dbFile.absolutePath}")
    }

    private fun initDatabase() {
        getConnection().use { conn ->
            conn.createStatement().use { stmt ->
                stmt.executeUpdate(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        role TEXT NOT NULL,
                        badge_number TEXT,
                        phone TEXT,
                        email TEXT
                    )
                    """.trimIndent()
                )

                stmt.executeUpdate(
                    """
                    CREATE TABLE IF NOT EXISTS theft_reports (
                        reference_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        category TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        status TEXT NOT NULL,
                        address TEXT NOT NULL,
                        landmark TEXT NOT NULL,
                        gps_coordinates TEXT,
                        suspect_consumer_number TEXT,
                        description TEXT NOT NULL,
                        evidence_image_data TEXT,
                        evidence_file_name TEXT,
                        is_anonymous INTEGER NOT NULL,
                        submitted_by_username TEXT,
                        reporter_name TEXT,
                        reporter_phone TEXT,
                        reporter_email TEXT,
                        assigned_officer TEXT,
                        assigned_officer_username TEXT,
                        inspection_notes TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        history_json TEXT NOT NULL
                    )
                    """.trimIndent()
                )
            }
        }
    }

    private fun seedUsersIfNeeded() {
        getConnection().use { conn ->
            val rs = conn.createStatement().executeQuery("SELECT COUNT(*) FROM users")
            val count = if (rs.next()) rs.getInt(1) else 0
            if (count > 0) return

            val defaultUsers = listOf(
                Pair(UserAccount("admin", "Chief Vigilance Administrator", UserRole.ADMIN, "ADM-HQ-01", "+91 11-23004400", "admin@powerguard.gov.in"), "admin123"),
                Pair(UserAccount("officer1", "Er. Vikramaditya Deshmukh", UserRole.OFFICER, "VIG-EI-09", "+91 98110-44203", "vikram.d@powerguard.gov.in"), "officer123"),
                Pair(UserAccount("officer2", "Er. Priya Nair", UserRole.OFFICER, "VIG-CC-01", "+91 98110-44202", "priya.nair@powerguard.gov.in"), "officer123"),
                Pair(UserAccount("officer3", "Er. Rajesh Sharma", UserRole.OFFICER, "VIG-NZ-04", "+91 98110-44201", "rajesh.sharma@powerguard.gov.in"), "officer123"),
                Pair(UserAccount("officer4", "Er. Ananya Verma", UserRole.OFFICER, "VIG-SR-12", "+91 98110-44204", "ananya.verma@powerguard.gov.in"), "officer123"),
                Pair(UserAccount("officer5", "Er. Mohammed Farooq", UserRole.OFFICER, "VIG-WR-07", "+91 98110-44205", "m.farooq@powerguard.gov.in"), "officer123"),
                Pair(UserAccount("citizen", "Rohan Deshmukh", UserRole.CITIZEN, null, "+91 98200-11223", "rohan.citizen@example.com"), "citizen123")
            )

            val sql = "INSERT OR REPLACE INTO users (username, password, full_name, role, badge_number, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)"
            conn.prepareStatement(sql).use { ps ->
                for ((u, pwd) in defaultUsers) {
                    ps.setString(1, u.username)
                    ps.setString(2, pwd)
                    ps.setString(3, u.fullName)
                    ps.setString(4, u.role.name)
                    ps.setString(5, u.badgeNumber)
                    ps.setString(6, u.phone)
                    ps.setString(7, u.email)
                    ps.executeUpdate()
                }
            }
        }
    }

    @Synchronized
    fun authenticate(req: LoginRequest): AuthResponse? {
        val uname = req.username.trim().lowercase()
        getConnection().use { conn ->
            conn.prepareStatement("SELECT * FROM users WHERE LOWER(username) = ? AND password = ?").use { ps ->
                ps.setString(1, uname)
                ps.setString(2, req.password.trim())
                val rs = ps.executeQuery()
                if (!rs.next()) return null

                val userRole = runCatching { UserRole.valueOf(rs.getString("role")) }.getOrDefault(UserRole.CITIZEN)
                if (req.role != null && req.role != userRole) {
                    return null
                }

                val account = UserAccount(
                    username = rs.getString("username"),
                    fullName = rs.getString("full_name"),
                    role = userRole,
                    badgeNumber = rs.getString("badge_number"),
                    phone = rs.getString("phone"),
                    email = rs.getString("email")
                )
                val token = "pg-token-${account.role.name.lowercase()}-${UUID.randomUUID().toString().take(8)}"
                return AuthResponse(token = token, user = account)
            }
        }
    }

    @Synchronized
    fun registerCitizen(req: RegisterCitizenRequest): Result<AuthResponse> {
        val uname = req.username.trim().lowercase()
        if (uname.length < 3 || req.password.length < 4 || req.fullName.isBlank()) {
            return Result.failure(IllegalArgumentException("Username (min 3 chars), password (min 4 chars), and full name are required."))
        }

        getConnection().use { conn ->
            conn.prepareStatement("SELECT username FROM users WHERE LOWER(username) = ?").use { checkPs ->
                checkPs.setString(1, uname)
                if (checkPs.executeQuery().next()) {
                    return Result.failure(IllegalArgumentException("Username '$uname' is already registered."))
                }
            }

            val account = UserAccount(
                username = uname,
                fullName = req.fullName.trim(),
                role = UserRole.CITIZEN,
                badgeNumber = null,
                phone = req.phone.trim().ifBlank { null },
                email = req.email.trim().ifBlank { null }
            )

            conn.prepareStatement(
                "INSERT INTO users (username, password, full_name, role, badge_number, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)"
            ).use { ps ->
                ps.setString(1, account.username)
                ps.setString(2, req.password.trim())
                ps.setString(3, account.fullName)
                ps.setString(4, account.role.name)
                ps.setString(5, null)
                ps.setString(6, account.phone)
                ps.setString(7, account.email)
                ps.executeUpdate()
            }

            val token = "pg-token-citizen-${UUID.randomUUID().toString().take(8)}"
            return Result.success(AuthResponse(token = token, user = account))
        }
    }

    @Synchronized
    fun getAllReports(
        status: String? = null,
        category: String? = null,
        severity: String? = null,
        search: String? = null,
        assignedOfficerUsername: String? = null,
        submittedByUsername: String? = null
    ): List<TheftReport> {
        val reports = mutableListOf<TheftReport>()
        getConnection().use { conn ->
            conn.createStatement().use { stmt ->
                val rs = stmt.executeQuery("SELECT * FROM theft_reports ORDER BY created_at DESC")
                while (rs.next()) {
                    val historyJson = rs.getString("history_json") ?: "[]"
                    val historyList = runCatching {
                        json.decodeFromString<List<StatusHistoryEntry>>(historyJson)
                    }.getOrDefault(emptyList())

                    reports.add(
                        TheftReport(
                            referenceId = rs.getString("reference_id"),
                            title = rs.getString("title"),
                            category = runCatching { TheftCategory.valueOf(rs.getString("category")) }.getOrDefault(TheftCategory.OTHER),
                            severity = runCatching { SeverityLevel.valueOf(rs.getString("severity")) }.getOrDefault(SeverityLevel.MEDIUM),
                            status = runCatching { ReportStatus.valueOf(rs.getString("status")) }.getOrDefault(ReportStatus.SUBMITTED),
                            address = rs.getString("address"),
                            landmark = rs.getString("landmark") ?: "",
                            gpsCoordinates = rs.getString("gps_coordinates"),
                            suspectConsumerNumber = rs.getString("suspect_consumer_number"),
                            description = rs.getString("description"),
                            evidenceImageData = rs.getString("evidence_image_data"),
                            evidenceFileName = rs.getString("evidence_file_name"),
                            isAnonymous = rs.getInt("is_anonymous") == 1,
                            submittedByUsername = rs.getString("submitted_by_username"),
                            reporterName = rs.getString("reporter_name"),
                            reporterPhone = rs.getString("reporter_phone"),
                            reporterEmail = rs.getString("reporter_email"),
                            assignedOfficer = rs.getString("assigned_officer"),
                            assignedOfficerUsername = rs.getString("assigned_officer_username"),
                            inspectionNotes = rs.getString("inspection_notes"),
                            createdAt = rs.getString("created_at"),
                            updatedAt = rs.getString("updated_at"),
                            history = historyList
                        )
                    )
                }
            }
        }

        return reports.filter { report ->
            val matchesStatus = status.isNullOrBlank() || status == "ALL" ||
                (status == "UNASSIGNED" && report.assignedOfficer.isNullOrBlank()) ||
                report.status.name.equals(status, ignoreCase = true)
            val matchesCategory = category.isNullOrBlank() || category == "ALL" || report.category.name.equals(category, ignoreCase = true)
            val matchesSeverity = severity.isNullOrBlank() || severity == "ALL" || report.severity.name.equals(severity, ignoreCase = true)
            val matchesOfficer = assignedOfficerUsername.isNullOrBlank() || assignedOfficerUsername == "ALL" ||
                report.assignedOfficerUsername.equals(assignedOfficerUsername, ignoreCase = true) ||
                report.assignedOfficer.equals(assignedOfficerUsername, ignoreCase = true)
            val matchesSubmitter = submittedByUsername.isNullOrBlank() ||
                report.submittedByUsername.equals(submittedByUsername, ignoreCase = true)

            val matchesSearch = search.isNullOrBlank() || listOfNotNull(
                report.referenceId,
                report.title,
                report.address,
                report.landmark,
                report.suspectConsumerNumber,
                report.assignedOfficer,
                report.description
            ).any { it.contains(search.trim(), ignoreCase = true) }

            matchesStatus && matchesCategory && matchesSeverity && matchesOfficer && matchesSubmitter && matchesSearch
        }
    }

    @Synchronized
    fun getReportByReferenceId(referenceId: String): TheftReport? {
        val normalized = referenceId.trim().uppercase()
        return getAllReports().find { it.referenceId.uppercase() == normalized }
    }

    @Synchronized
    fun createReport(req: CreateReportRequest): TheftReport {
        val now = LocalDateTime.now().format(formatter)
        val referenceId = generateUniqueReferenceId()
        val reporterDisplayName = req.reporterName?.trim()?.takeIf { it.isNotEmpty() }
            ?: req.submittedByUsername
            ?: "Citizen"
        val initialHistory = listOf(
            StatusHistoryEntry(
                timestamp = now,
                status = ReportStatus.SUBMITTED,
                updatedBy = reporterDisplayName,
                remarks = "Electricity theft complaint registered by $reporterDisplayName. Forwarded to Administrator for Vigilance Officer assignment."
            )
        )

        val report = TheftReport(
            referenceId = referenceId,
            title = req.title.trim(),
            category = req.category,
            severity = req.severity,
            status = ReportStatus.SUBMITTED,
            address = req.address.trim(),
            landmark = req.landmark.trim(),
            gpsCoordinates = req.gpsCoordinates?.trim()?.takeIf { it.isNotEmpty() },
            suspectConsumerNumber = req.suspectConsumerNumber?.trim()?.takeIf { it.isNotEmpty() },
            description = req.description.trim(),
            evidenceImageData = req.evidenceImageData?.takeIf { it.isNotBlank() },
            evidenceFileName = req.evidenceFileName?.takeIf { it.isNotBlank() },
            isAnonymous = false,
            submittedByUsername = req.submittedByUsername?.trim()?.takeIf { it.isNotBlank() },
            reporterName = req.reporterName?.trim()?.takeIf { it.isNotEmpty() } ?: reporterDisplayName,
            reporterPhone = req.reporterPhone?.trim(),
            reporterEmail = req.reporterEmail?.trim(),
            assignedOfficer = null,
            assignedOfficerUsername = null,
            inspectionNotes = "Awaiting Administrator assignment to a Field Vigilance Officer.",
            createdAt = now,
            updatedAt = now,
            history = initialHistory
        )

        saveOrUpdateReport(report)
        syncJsonMirror()
        return report
    }

    @Synchronized
    fun assignOfficerByAdmin(referenceId: String, req: AdminAssignOfficerRequest): TheftReport? {
        val existing = getReportByReferenceId(referenceId) ?: return null
        val now = LocalDateTime.now().format(formatter)

        val matchedOfficer = officers.find {
            it.username.equals(req.assignedOfficerUsername, ignoreCase = true) ||
                it.name.equals(req.assignedOfficer, ignoreCase = true)
        }
        val officerName = matchedOfficer?.name ?: req.assignedOfficer.trim()
        val officerUsername = matchedOfficer?.username ?: req.assignedOfficerUsername

        val nextStatus = if (existing.status == ReportStatus.SUBMITTED) {
            ReportStatus.UNDER_INVESTIGATION
        } else {
            existing.status
        }

        val adminNote = req.adminRemarks?.takeIf { it.isNotBlank() }
            ?: "Assigned to Vigilance Officer $officerName for field inspection and verification."

        val newEntry = StatusHistoryEntry(
            timestamp = now,
            status = nextStatus,
            updatedBy = "${req.updatedBy} (Admin)",
            remarks = "Assigned to $officerName. Instructions: $adminNote"
        )

        val updated = existing.copy(
            status = nextStatus,
            severity = req.severity ?: existing.severity,
            assignedOfficer = officerName,
            assignedOfficerUsername = officerUsername,
            inspectionNotes = adminNote,
            updatedAt = now,
            history = existing.history + newEntry
        )

        saveOrUpdateReport(updated)
        syncJsonMirror()
        return updated
    }

    @Synchronized
    fun investigateReportByOfficer(referenceId: String, req: OfficerInvestigationRequest): TheftReport? {
        val existing = getReportByReferenceId(referenceId) ?: return null
        val now = LocalDateTime.now().format(formatter)

        val newEntry = StatusHistoryEntry(
            timestamp = now,
            status = req.status,
            updatedBy = "${req.updatedBy} (Vigilance Officer)",
            remarks = req.inspectionNotes.trim()
        )

        val updated = existing.copy(
            status = req.status,
            inspectionNotes = req.inspectionNotes.trim(),
            updatedAt = now,
            history = existing.history + newEntry
        )

        saveOrUpdateReport(updated)
        syncJsonMirror()
        return updated
    }

    @Synchronized
    fun updateReportStatus(referenceId: String, req: UpdateReportStatusRequest): TheftReport? {
        val existing = getReportByReferenceId(referenceId) ?: return null
        val now = LocalDateTime.now().format(formatter)

        val matchedOfficer = officers.find {
            it.username.equals(req.assignedOfficerUsername, ignoreCase = true) ||
                it.name.equals(req.assignedOfficer, ignoreCase = true)
        }

        val defaultRemark = when (req.status) {
            ReportStatus.SUBMITTED -> "Report queued for officer assignment."
            ReportStatus.UNDER_INVESTIGATION -> "Case assigned for vigilance verification."
            ReportStatus.TEAM_DISPATCHED -> "Field vigilance squad dispatched to inspect site."
            ReportStatus.RESOLVED_CONFIRMED -> "Electricity theft confirmed on site and action completed."
            ReportStatus.DISMISSED -> "Site inspection completed. No unauthorized tapping detected."
        }

        val newEntry = StatusHistoryEntry(
            timestamp = now,
            status = req.status,
            updatedBy = req.updatedBy.ifBlank { req.assignedOfficer ?: "Vigilance Control Room" },
            remarks = req.inspectionNotes?.takeIf { it.isNotBlank() } ?: defaultRemark
        )

        val updated = existing.copy(
            status = req.status,
            assignedOfficer = matchedOfficer?.name ?: req.assignedOfficer?.takeIf { it.isNotBlank() } ?: existing.assignedOfficer,
            assignedOfficerUsername = matchedOfficer?.username ?: req.assignedOfficerUsername ?: existing.assignedOfficerUsername,
            inspectionNotes = req.inspectionNotes?.takeIf { it.isNotBlank() } ?: existing.inspectionNotes,
            updatedAt = now,
            history = existing.history + newEntry
        )

        saveOrUpdateReport(updated)
        syncJsonMirror()
        return updated
    }

    @Synchronized
    fun deleteReport(referenceId: String): Boolean {
        val normalized = referenceId.trim().uppercase()
        getConnection().use { conn ->
            conn.prepareStatement("DELETE FROM theft_reports WHERE UPPER(reference_id) = ?").use { ps ->
                ps.setString(1, normalized)
                val rows = ps.executeUpdate()
                if (rows > 0) {
                    syncJsonMirror()
                    return true
                }
                return false
            }
        }
    }

    @Synchronized
    fun getDashboardStats(): DashboardStats {
        val all = getAllReports()
        val unassigned = all.count { it.assignedOfficer.isNullOrBlank() }
        val pending = all.count { it.status == ReportStatus.SUBMITTED }
        val active = all.count { it.status == ReportStatus.UNDER_INVESTIGATION || it.status == ReportStatus.TEAM_DISPATCHED }
        val resolved = all.count { it.status == ReportStatus.RESOLVED_CONFIRMED }
        val dismissed = all.count { it.status == ReportStatus.DISMISSED }

        val categoryBreakdown = TheftCategory.entries.associate { cat ->
            cat.displayName to all.count { it.category == cat }
        }.filterValues { it > 0 }

        val statusBreakdown = ReportStatus.entries.associate { st ->
            st.displayName to all.count { it.status == st }
        }
        val severityBreakdown = SeverityLevel.entries.associate { sev ->
            sev.displayName to all.count { it.severity == sev }
        }

        return DashboardStats(
            totalReports = all.size,
            unassignedCases = unassigned,
            pendingCases = pending,
            activeInvestigations = active,
            resolvedCases = resolved,
            dismissedCases = dismissed,
            categoryBreakdown = categoryBreakdown,
            statusBreakdown = statusBreakdown,
            severityBreakdown = severityBreakdown
        )
    }

    private fun saveOrUpdateReport(report: TheftReport) {
        val sql = """
            INSERT OR REPLACE INTO theft_reports (
                reference_id, title, category, severity, status, address, landmark,
                gps_coordinates, suspect_consumer_number, description,
                evidence_image_data, evidence_file_name, is_anonymous, submitted_by_username,
                reporter_name, reporter_phone, reporter_email, assigned_officer,
                assigned_officer_username, inspection_notes, created_at, updated_at, history_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """.trimIndent()

        getConnection().use { conn ->
            conn.prepareStatement(sql).use { ps ->
                ps.setString(1, report.referenceId)
                ps.setString(2, report.title)
                ps.setString(3, report.category.name)
                ps.setString(4, report.severity.name)
                ps.setString(5, report.status.name)
                ps.setString(6, report.address)
                ps.setString(7, report.landmark)
                ps.setString(8, report.gpsCoordinates)
                ps.setString(9, report.suspectConsumerNumber)
                ps.setString(10, report.description)
                ps.setString(11, report.evidenceImageData)
                ps.setString(12, report.evidenceFileName)
                ps.setInt(13, if (report.isAnonymous) 1 else 0)
                ps.setString(14, report.submittedByUsername)
                ps.setString(15, report.reporterName)
                ps.setString(16, report.reporterPhone)
                ps.setString(17, report.reporterEmail)
                ps.setString(18, report.assignedOfficer)
                ps.setString(19, report.assignedOfficerUsername)
                ps.setString(20, report.inspectionNotes)
                ps.setString(21, report.createdAt)
                ps.setString(22, report.updatedAt)
                ps.setString(23, json.encodeToString(report.history))
                ps.executeUpdate()
            }
        }
        saveEvidenceImageFile(report.referenceId, report.evidenceFileName, report.evidenceImageData)
    }

    private fun saveEvidenceImageFile(referenceId: String, fileName: String?, base64Data: String?) {
        if (base64Data.isNullOrBlank() || !base64Data.contains(",")) return
        runCatching {
            val imagesDir = File(dataDir, "evidence_images")
            if (!imagesDir.exists()) imagesDir.mkdirs()
            val parts = base64Data.split(",", limit = 2)
            val header = parts[0]
            val rawBase64 = parts[1]
            val ext = if (header.contains("png", ignoreCase = true)) ".png" else ".jpg"
            val cleanName = (fileName?.takeIf { it.isNotBlank() } ?: "evidence$ext")
                .replace(Regex("[^a-zA-Z0-9._-]"), "_")
            val targetFile = File(imagesDir, "${referenceId}_$cleanName")
            val bytes = java.util.Base64.getDecoder().decode(rawBase64)
            targetFile.writeBytes(bytes)
        }.onFailure {
            logger.warn("Could not save evidence image file: ${it.message}")
        }
    }

    private fun syncJsonMirror() {
        runCatching {
            val all = getAllReports()
            val jsonText = json.encodeToString(all)
            jsonMirrorFile.writeText(jsonText)

            if (dbHtmlFile.exists()) {
                val html = dbHtmlFile.readText()
                val regex = Regex("let allReports = \\[.*?\\];", RegexOption.DOT_MATCHES_ALL)
                if (regex.containsMatchIn(html)) {
                    val updated = regex.replace(html, "let allReports = $jsonText;")
                    dbHtmlFile.writeText(updated)
                }
            }
        }.onFailure {
            logger.warn("Could not write JSON mirror or DB HTML file: ${it.message}")
        }
    }

    private fun generateUniqueReferenceId(): String {
        val existingIds = getAllReports().map { it.referenceId }.toSet()
        var candidate: String
        do {
            val num = Random.nextInt(1000, 9999)
            candidate = "PG-2026-$num"
        } while (candidate in existingIds)
        return candidate
    }
}
