package com.powerguard.models

import kotlinx.serialization.Serializable

@Serializable
enum class UserRole(val displayName: String) {
    CITIZEN("Citizen"),
    OFFICER("Vigilance Officer"),
    ADMIN("Administrator")
}

@Serializable
data class UserAccount(
    val username: String,
    val fullName: String,
    val role: UserRole,
    val badgeNumber: String? = null,
    val phone: String? = null,
    val email: String? = null
)

@Serializable
data class LoginRequest(
    val username: String,
    val password: String,
    val role: UserRole? = null
)

@Serializable
data class RegisterCitizenRequest(
    val username: String,
    val password: String,
    val fullName: String,
    val phone: String = "",
    val email: String = ""
)

@Serializable
data class AuthResponse(
    val token: String,
    val user: UserAccount
)

@Serializable
enum class TheftCategory(val displayName: String) {
    DIRECT_HOOKING("Direct Line Hooking (Kundi)"),
    METER_TAMPERING("Meter Tampering / Bypass"),
    ILLEGAL_SUB_METERING("Illegal Commercial Sub-Metering"),
    TRANSFORMER_TAP("Unauthorized Transformer Tap"),
    SEAL_BROKEN("Broken / Forged Meter Seal"),
    UNDERGROUND_CABLE_TAP("Underground Cable Splicing"),
    OTHER("Other Suspicious Consumption")
}

@Serializable
enum class SeverityLevel(val displayName: String, val priorityScore: Int) {
    LOW("Low", 1),
    MEDIUM("Medium", 2),
    HIGH("High", 3),
    CRITICAL("Critical", 4)
}

@Serializable
enum class ReportStatus(val displayName: String) {
    SUBMITTED("Submitted (Pending Assignment)"),
    UNDER_INVESTIGATION("Assigned & Under Investigation"),
    TEAM_DISPATCHED("Field Team Dispatched"),
    RESOLVED_CONFIRMED("Resolved (Theft Confirmed)"),
    DISMISSED("Dismissed (No Violation Found)")
}

@Serializable
data class StatusHistoryEntry(
    val timestamp: String,
    val status: ReportStatus,
    val updatedBy: String,
    val remarks: String
)

@Serializable
data class TheftReport(
    val referenceId: String,
    val title: String,
    val category: TheftCategory,
    val severity: SeverityLevel,
    val status: ReportStatus,
    val address: String,
    val landmark: String,
    val gpsCoordinates: String? = null,
    val suspectConsumerNumber: String? = null,
    val description: String,
    val evidenceImageData: String? = null,
    val evidenceFileName: String? = null,
    val isAnonymous: Boolean = false,
    val submittedByUsername: String? = null,
    val reporterName: String? = null,
    val reporterPhone: String? = null,
    val reporterEmail: String? = null,
    val assignedOfficer: String? = null,
    val assignedOfficerUsername: String? = null,
    val inspectionNotes: String? = null,
    val createdAt: String,
    val updatedAt: String,
    val history: List<StatusHistoryEntry> = emptyList()
)

@Serializable
data class PublicTrackingResponse(
    val referenceId: String,
    val title: String,
    val category: TheftCategory,
    val categoryDisplay: String,
    val severity: SeverityLevel,
    val status: ReportStatus,
    val statusDisplay: String,
    val address: String,
    val landmark: String,
    val assignedOfficer: String?,
    val inspectionNotes: String?,
    val createdAt: String,
    val updatedAt: String,
    val history: List<StatusHistoryEntry>
)

@Serializable
data class CreateReportRequest(
    val title: String,
    val category: TheftCategory,
    val severity: SeverityLevel,
    val address: String,
    val landmark: String = "",
    val gpsCoordinates: String? = null,
    val suspectConsumerNumber: String? = null,
    val description: String,
    val evidenceImageData: String? = null,
    val evidenceFileName: String? = null,
    val isAnonymous: Boolean = false,
    val submittedByUsername: String? = null,
    val reporterName: String? = null,
    val reporterPhone: String? = null,
    val reporterEmail: String? = null
)

@Serializable
data class AdminAssignOfficerRequest(
    val assignedOfficer: String,
    val assignedOfficerUsername: String? = null,
    val severity: SeverityLevel? = null,
    val adminRemarks: String? = null,
    val updatedBy: String = "Administrator"
)

@Serializable
data class OfficerInvestigationRequest(
    val status: ReportStatus,
    val inspectionNotes: String,
    val updatedBy: String = "Vigilance Officer"
)

@Serializable
data class UpdateReportStatusRequest(
    val status: ReportStatus,
    val assignedOfficer: String? = null,
    val assignedOfficerUsername: String? = null,
    val inspectionNotes: String? = null,
    val updatedBy: String = "Vigilance Inspector"
)

@Serializable
data class VigilanceOfficer(
    val id: String,
    val username: String,
    val name: String,
    val badgeNumber: String,
    val designation: String,
    val contact: String
)

@Serializable
data class DashboardStats(
    val totalReports: Int,
    val unassignedCases: Int,
    val pendingCases: Int,
    val activeInvestigations: Int,
    val resolvedCases: Int,
    val dismissedCases: Int,
    val categoryBreakdown: Map<String, Int>,
    val statusBreakdown: Map<String, Int>,
    val severityBreakdown: Map<String, Int>
)

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val message: String,
    val data: T? = null
)
