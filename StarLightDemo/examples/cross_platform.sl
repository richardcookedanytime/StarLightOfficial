// Starlight 语言 - 跨平台示例
// 展示同一份源码在不同平台的编译和运行

// 平台无关的通用代码
expect class PlatformInfo {
    fun getOSName(): String
    fun getArchitecture(): String
    fun getCurrentTime(): Long
}

expect fun logMessage(level: String, message: String): Unit

// 平台特定的实现
// JVM 实现
actual class PlatformInfo {
    actual fun getOSName(): String = System.getProperty("os.name")
    actual fun getArchitecture(): String = System.getProperty("os.arch")
    actual fun getCurrentTime(): Long = System.currentTimeMillis()
}

actual fun logMessage(level: String, message: String) {
    println("[${level.toUpperCase()}] ${LocalDateTime.now()}: $message")
}

// JavaScript 实现
actual class PlatformInfo {
    actual fun getOSName(): String {
        return if (typeof navigator !== "undefined") {
            navigator.platform
        } else {
            "Node.js"
        }
    }
    
    actual fun getArchitecture(): String {
        return if (typeof navigator !== "undefined") {
            navigator.userAgent
        } else {
            process.arch
        }
    }
    
    actual fun getCurrentTime(): Long = Date.now()
}

actual fun logMessage(level: String, message: String) {
    if (typeof console !== "undefined") {
        console.log(`[${level.toUpperCase()}] ${new Date().toISOString()}: ${message}`)
    }
}

// WebAssembly 实现
actual class PlatformInfo {
    actual fun getOSName(): String = "WASM"
    actual fun getArchitecture(): String = "wasm32"
    actual fun getCurrentTime(): Long = wasmtime.getCurrentTime()
}

actual fun logMessage(level: String, message: String) {
    wasmtime.log(level, message)
}

// 统一的异步 API
expect class HttpClient {
    fun get(url: String): Promise<String>
    fun post(url: String, data: String): Promise<String>
}

// JVM 实现 - 使用 CompletableFuture
actual class HttpClient {
    private val client = HttpClient.newHttpClient()
    
    actual fun get(url: String): Promise<String> {
        val request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .GET()
            .build()
        
        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply { it.body() }
    }
    
    actual fun post(url: String, data: String): Promise<String> {
        val request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(data))
            .build()
        
        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply { it.body() }
    }
}

// JavaScript 实现 - 使用 fetch API
actual class HttpClient {
    actual fun get(url: String): Promise<String> {
        return fetch(url)
            .then { response -> response.text() }
    }
    
    actual fun post(url: String, data: String): Promise<String> {
        return fetch(url, object {
            method = "POST"
            headers = mapOf("Content-Type" to "application/json")
            body = data
        }).then { response -> response.text() }
    }
}

// 文件系统操作
expect class FileSystem {
    fun readFile(path: String): String
    fun writeFile(path: String, content: String): Unit
    fun exists(path: String): Boolean
}

// JVM 实现
actual class FileSystem {
    actual fun readFile(path: String): String {
        return Files.readString(Paths.get(path))
    }
    
    actual fun writeFile(path: String, content: String) {
        Files.write(Paths.get(path), content.toByteArray())
    }
    
    actual fun exists(path: String): Boolean {
        return Files.exists(Paths.get(path))
    }
}

// JavaScript 实现
actual class FileSystem {
    actual fun readFile(path: String): String {
        return if (typeof require !== "undefined") {
            // Node.js 环境
            require("fs").readFileSync(path, "utf8")
        } else {
            // 浏览器环境 - 使用 File API
            throw UnsupportedOperationException("File reading not supported in browser")
        }
    }
    
    actual fun writeFile(path: String, content: String) {
        if (typeof require !== "undefined") {
            require("fs").writeFileSync(path, content, "utf8")
        } else {
            // 浏览器环境 - 触发下载
            val blob = new Blob([content], object { type = "text/plain" })
            val url = URL.createObjectURL(blob)
            val a = document.createElement("a")
            a.href = url
            a.download = path
            a.click()
            URL.revokeObjectURL(url)
        }
    }
    
    actual fun exists(path: String): Boolean {
        return if (typeof require !== "undefined") {
            require("fs").existsSync(path)
        } else {
            false
        }
    }
}

// 跨平台应用示例
class CrossPlatformApp {
    private val platformInfo = PlatformInfo()
    private val httpClient = HttpClient()
    private val fileSystem = FileSystem()
    
    suspend fun run() {
        logMessage("info", "应用启动")
        
        // 显示平台信息
        println("=== 平台信息 ===")
        println("操作系统: ${platformInfo.getOSName()}")
        println("架构: ${platformInfo.getArchitecture()}")
        println("当前时间: ${platformInfo.getCurrentTime()}")
        
        // HTTP 请求示例
        try {
            logMessage("info", "发送 HTTP 请求")
            val response = httpClient.get("https://api.github.com/zen")
            logMessage("info", "收到响应: $response")
        } catch (e: Exception) {
            logMessage("error", "HTTP 请求失败: ${e.message}")
        }
        
        // 文件操作示例
        try {
            val configPath = "config.json"
            if (fileSystem.exists(configPath)) {
                val content = fileSystem.readFile(configPath)
                logMessage("info", "读取配置文件: $content")
            } else {
                val defaultConfig = """{
                    "app": "Starlight Cross-Platform Demo",
                    "version": "1.0.0",
                    "platform": "${platformInfo.getOSName()}"
                }"""
                fileSystem.writeFile(configPath, defaultConfig)
                logMessage("info", "创建默认配置文件")
            }
        } catch (e: Exception) {
            logMessage("error", "文件操作失败: ${e.message}")
        }
        
        // 平台特定的功能演示
        demonstratePlatformFeatures()
        
        logMessage("info", "应用结束")
    }
    
    private fun demonstratePlatformFeatures() {
        when (platformInfo.getOSName()) {
            "Windows" -> {
                logMessage("info", "运行 Windows 特定功能")
                // Windows 特定代码
            }
            "Mac OS X" -> {
                logMessage("info", "运行 macOS 特定功能")
                // macOS 特定代码
            }
            "Linux" -> {
                logMessage("info", "运行 Linux 特定功能")
                // Linux 特定代码
            }
            "Node.js" -> {
                logMessage("info", "运行 Node.js 特定功能")
                // Node.js 特定代码
            }
            "WASM" -> {
                logMessage("info", "运行 WebAssembly 特定功能")
                // WASM 特定代码
            }
            else -> {
                logMessage("warn", "未知平台: ${platformInfo.getOSName()}")
            }
        }
    }
}

// 主函数 - 在不同平台有不同的入口点
// JVM 入口
fun main(args: Array<String>) {
    runBlocking {
        val app = CrossPlatformApp()
        app.run()
    }
}

// JavaScript 入口
fun main() {
    CrossPlatformApp().run()
}

// WebAssembly 入口
@Export("wasm_main")
fun wasmMain() {
    CrossPlatformApp().run()
}

// 构建配置示例
// starlight.json
val buildConfig = """
{
    "name": "cross-platform-demo",
    "version": "1.0.0",
    "targets": {
        "jvm": {
            "main": "main",
            "output": "build/demo.jar"
        },
        "js": {
            "main": "main",
            "output": "build/demo.js",
            "format": "esm"
        },
        "wasm": {
            "main": "wasmMain",
            "output": "build/demo.wasm"
        }
    },
    "dependencies": {
        "jvm": ["org.springframework:spring-boot-starter:3.0.0"],
        "js": [],
        "wasm": []
    }
}
"""
