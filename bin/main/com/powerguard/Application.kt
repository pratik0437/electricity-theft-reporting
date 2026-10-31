package com.powerguard

import com.powerguard.models.ApiResponse
import com.powerguard.routes.configureApiRoutes
import com.powerguard.storage.ReportRepository
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.http.content.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.calllogging.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.plugins.statuspages.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.json.Json
import java.io.File

fun main() {
    val port = System.getenv("PORT")?.toIntOrNull() ?: 8080
    println("==================================================================")
    println("  PowerGuard - Electricity Theft Reporting & Vigilance System")
    println("  Backend Stack : Kotlin ${KotlinVersion.CURRENT} + Ktor + SQLite")
    println("  Web Portal URL: http://localhost:$port")
    println("==================================================================")

    embeddedServer(Netty, port = port, host = "0.0.0.0", module = Application::module)
        .start(wait = true)
}

fun Application.module() {
    val repository = ReportRepository(File("data"))

    install(CallLogging)

    install(ContentNegotiation) {
        json(
            Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
                encodeDefaults = true
            }
        )
    }

    install(CORS) {
        anyHost()
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowMethod(HttpMethod.Get)
        allowMethod(HttpMethod.Post)
        allowMethod(HttpMethod.Patch)
        allowMethod(HttpMethod.Put)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Options)
    }

    install(StatusPages) {
        exception<Throwable> { call, cause ->
            call.application.environment.log.error("Unhandled exception", cause)
            call.respond(
                HttpStatusCode.InternalServerError,
                ApiResponse<String>(
                    success = false,
                    message = "Internal Server Error: ${cause.localizedMessage ?: "Unexpected error"}"
                )
            )
        }
    }

    routing {
        configureApiRoutes(repository)
        staticResources("/", "static", index = "index.html")
    }
}
