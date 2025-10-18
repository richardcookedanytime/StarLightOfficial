// Starlight 语言 - Java 互操作示例
// 展示与 Java 生态系统的无缝集成

// 直接导入 Java 类，无需桥接层
import java.util.ArrayList
import java.util.HashMap
import java.util.stream.Collectors
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import javax.servlet.annotation.WebServlet
import javax.servlet.http.HttpServlet
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse
import javax.servlet.ServletException
import java.io.IOException

// Spring Boot 集成示例
import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.http.ResponseEntity

// 直接实现 Java 接口
class JavaInteropDemo {
    
    // 使用 Java Collections
    fun demonstrateCollections(): List<String> {
        val list = ArrayList<String>()
        list.add("Hello")
        list.add("Java")
        list.add("World")
        
        val map = HashMap<String, Int>()
        map["count"] = 42
        map["version"] = 17
        
        // 使用 Java Stream API
        return list.stream()
            .filter { it.length > 4 }
            .map { it.uppercase() }
            .collect(Collectors.toList())
    }
    
    // 使用 Java Time API
    fun getCurrentDateTime(): String {
        val now = LocalDateTime.now()
        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
        return now.format(formatter)
    }
    
    // 使用 Java 8+ 特性
    fun processNumbers(): List<Int> {
        val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        
        return numbers.stream()
            .filter { it % 2 == 0 }
            .map { it * it }
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList())
    }
}

// Servlet 示例 - 直接继承 Java Servlet
@WebServlet("/api/time")
class TimeServlet : HttpServlet() {
    
    @Throws(ServletException::class, IOException::class)
    override fun doGet(req: HttpServletRequest, resp: HttpServletResponse) {
        resp.contentType = "application/json"
        resp.characterEncoding = "UTF-8"
        
        val timeInfo = mapOf(
            "currentTime" to LocalDateTime.now().toString(),
            "currentDate" to LocalDate.now().toString(),
            "timestamp" to System.currentTimeMillis()
        )
        
        resp.writer.write(gson.toJson(timeInfo))
    }
}

// Spring Boot 控制器示例
@SpringBootApplication
@RestController
class StarlightSpringApp {
    
    private val userService = UserService()
    
    @GetMapping("/api/users")
    fun getAllUsers(): ResponseEntity<List<User>> {
        val users = userService.findAll()
        return ResponseEntity.ok(users)
    }
    
    @GetMapping("/api/users/{id}")
    fun getUser(@PathVariable id: Long): ResponseEntity<User> {
        val user = userService.findById(id)
        return if (user != null) {
            ResponseEntity.ok(user)
        } else {
            ResponseEntity.notFound().build()
        }
    }
    
    @PostMapping("/api/users")
    fun createUser(@RequestBody userRequest: CreateUserRequest): ResponseEntity<User> {
        val user = userService.create(userRequest)
        return ResponseEntity.status(201).body(user)
    }
    
    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            SpringApplication.run(StarlightSpringApp::class.java, *args)
        }
    }
}

// 数据类 - 自动生成 Java Bean 方法
data class User(
    val id: Long?,
    val name: String,
    val email: String,
    val createdAt: LocalDateTime = LocalDateTime.now()
)

data class CreateUserRequest(
    val name: String,
    val email: String
)

// 服务类 - 使用 Java 注解
@Service
@Transactional
class UserService {
    
    @Autowired
    private lateinit var userRepository: UserRepository
    
    fun findAll(): List<User> {
        return userRepository.findAll().map { it.toDomain() }
    }
    
    fun findById(id: Long): User? {
        return userRepository.findById(id).orElse(null)?.toDomain()
    }
    
    fun create(request: CreateUserRequest): User {
        val entity = UserEntity(
            name = request.name,
            email = request.email
        )
        val saved = userRepository.save(entity)
        return saved.toDomain()
    }
}

// JPA 实体类
@Entity
@Table(name = "users")
data class UserEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,
    
    @Column(nullable = false)
    val name: String,
    
    @Column(nullable = false, unique = true)
    val email: String,
    
    @CreationTimestamp
    val createdAt: LocalDateTime = LocalDateTime.now()
) {
    fun toDomain(): User {
        return User(id, name, email, createdAt)
    }
}

// Repository 接口
interface UserRepository : JpaRepository<UserEntity, Long> {
    fun findByEmail(email: String): UserEntity?
    fun findByNameContaining(name: String): List<UserEntity>
}

// 使用 Java 8 函数式接口
class FunctionalInterop {
    
    fun demonstrateFunctionalInterfaces() {
        // Predicate
        val isEven: Predicate<Int> = { it % 2 == 0 }
        
        // Function
        val square: Function<Int, Int> = { it * it }
        
        // Consumer
        val printer: Consumer<String> = { println(it) }
        
        // Supplier
        val randomSupplier: Supplier<Int> = { Random().nextInt(100) }
        
        // 使用示例
        val numbers = listOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        
        numbers.stream()
            .filter(isEven)
            .map(square)
            .forEach { printer.accept(it.toString()) }
    }
}

// 异常处理 - 与 Java 异常系统完全兼容
class ExceptionHandling {
    
    fun demonstrateExceptionHandling() {
        try {
            // 可能抛出 Java 异常的操作
            val file = File("nonexistent.txt")
            val content = file.readText() // 可能抛出 IOException
            println(content)
        } catch (e: IOException) {
            println("文件读取失败: ${e.message}")
        } catch (e: SecurityException) {
            println("安全异常: ${e.message}")
        } finally {
            println("清理资源")
        }
    }
    
    // 抛出 Java 异常
    @Throws(IllegalArgumentException::class)
    fun validateAge(age: Int): String {
        if (age < 0 || age > 150) {
            throw IllegalArgumentException("年龄必须在 0-150 之间")
        }
        return "年龄有效: $age"
    }
}

// 使用示例
fun main(args: Array<String>) {
    val demo = JavaInteropDemo()
    
    println("=== Java Collections 演示 ===")
    val filteredList = demo.demonstrateCollections()
    println(filteredList)
    
    println("\n=== Java Time API 演示 ===")
    println("当前时间: ${demo.getCurrentDateTime()}")
    
    println("\n=== Java Stream API 演示 ===")
    val processedNumbers = demo.processNumbers()
    println(processedNumbers)
    
    println("\n=== 异常处理演示 ===")
    val exceptionDemo = ExceptionHandling()
    exceptionDemo.demonstrateExceptionHandling()
    
    try {
        exceptionDemo.validateAge(-5)
    } catch (e: IllegalArgumentException) {
        println("捕获异常: ${e.message}")
    }
    
    println("\n=== 函数式接口演示 ===")
    val functionalDemo = FunctionalInterop()
    functionalDemo.demonstrateFunctionalInterfaces()
}
