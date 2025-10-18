// Starlight 语言 - 完整特性展示
// 展示语法糖、逻辑化扩展和声明式编程

@version("1.0")
@feature("rules", enabled=true)
@feature("comprehensions", enabled=true)
@feature("transactions", enabled=true)

// ===== 1. 数据类和简洁语法 =====

data User(name: string, age: int, email: string?) {
    fun isAdult(): boolean = age >= 18
    
    fun getDisplayName(): string = if (name.isEmpty()) "Anonymous" else name
}

data Product(id: int, name: string, price: float, category: string) {
    fun isExpensive(): boolean = price > 100.0
    
    fun getFormattedPrice(): string = "$${price:.2f}"
}

// ===== 2. 规则系统和逻辑化编程 =====

// 业务规则定义
rule adult(User.age >= 18) => User.canVote = true
rule senior(User.age >= 65) => User.discount = 0.15
rule premium(Product.price > 500.0) => Product.shipping = 0.0

// 复杂规则组合
rule eligibility(user: User, product: Product) => {
    if (user.isAdult() && product.price <= user.budget) {
        user.canPurchase = true
        product.availableForUser = true
    }
}

// ===== 3. 扩展函数 =====

extend String {
    fun isEmail(): boolean = this.contains("@") && this.contains(".")
    
    fun capitalize(): string = this.substring(0, 1).toUpperCase() + this.substring(1)
    
    fun truncate(maxLength: int): string = 
        if (this.length <= maxLength) this 
        else this.substring(0, maxLength) + "..."
}

extend List<T> {
    fun filter(predicate: (T) -> boolean): List<T> {
        val result = ArrayList<T>()
        for (item in this) {
            if (predicate(item)) {
                result.add(item)
            }
        }
        return result
    }
    
    fun map<R>(transform: (T) -> R): List<R> {
        val result = ArrayList<R>()
        for (item in this) {
            result.add(transform(item))
        }
        return result
    }
}

// ===== 4. 列表推导式和管道操作 =====

fun processUsers(users: List<User>): List<string> {
    // 列表推导式
    return [user.name.capitalize() 
            | for user in users 
            if user.isAdult() && user.email != null]
}

fun calculateStatistics(products: List<Product>): Map<string, float> {
    return products
        | groupBy { it.category }
        | mapValues { categoryProducts -> 
            categoryProducts
                | map { it.price }
                | average()
          }
}

// ===== 5. 模式匹配 =====

fun handleUserAction(action: UserAction): string = match action {
    Login(username, password) => "User ${username} logged in"
    Logout(userId) => "User ${userId} logged out"
    Purchase(userId, productId, quantity) => 
        "User ${userId} purchased ${quantity} of product ${productId}"
    Search(query, filters) => "Searching for '${query}' with filters"
    _ => "Unknown action"
}

// ===== 6. 异步编程和协程 =====

async fun fetchUserProfile(userId: int): UserProfile {
    val user = await userService.getUser(userId)
    val preferences = await preferenceService.getPreferences(userId)
    val purchaseHistory = await purchaseService.getHistory(userId)
    
    return UserProfile(user, preferences, purchaseHistory)
}

async fun processBatch(requests: List<Request>): List<Response> {
    // 并发处理
    val tasks = requests.map { request -> 
        processRequest(request)
    }
    
    return await Promise.all(tasks)
}

// ===== 7. 事务处理 =====

fun transferMoney(fromAccount: Account, toAccount: Account, amount: float): boolean {
    return transaction {
        try {
            if (fromAccount.balance >= amount) {
                fromAccount.balance -= amount
                toAccount.balance += amount
                
                // 记录交易
                val transaction = Transaction(fromAccount.id, toAccount.id, amount)
                transactionService.record(transaction)
                
                true
            } else {
                false
            }
        } catch (e: Exception) {
            // 事务会自动回滚
            false
        }
    }
}

// ===== 8. 类型系统和泛型 =====

// 联合类型
type Result<T> = Success(T) | Error(string)

fun processResult(result: Result<User>): string = match result {
    Success(user) => "User: ${user.name}"
    Error(message) => "Error: ${message}"
}

// 类型别名
type UserId = int
type ProductId = int
type OrderId = string

// 泛型函数
fun <T, R> List<T>.mapNotNull(transform: (T) -> R?): List<R> {
    return this
        | map { transform(it) }
        | filter { it != null }
        | map { it!! }
}

// ===== 9. 平台特定实现 =====

// 声明平台相关函数
expect fun getCurrentTime(): long
expect fun showNotification(message: string): void
expect fun saveToStorage(key: string, value: string): void

// JVM 实现
actual fun getCurrentTime(): long = System.currentTimeMillis()
actual fun showNotification(message: string): void = println("Notification: ${message}")
actual fun saveToStorage(key: string, value: string): void = 
    System.setProperty(key, value)

// ===== 10. Java 互操作 =====

import java.util.stream.Collectors
import java.time.LocalDateTime
import javax.servlet.annotation.WebServlet
import javax.servlet.http.HttpServlet

@WebServlet("/api/users")
class UserServlet : HttpServlet() {
    
    override fun doGet(req: HttpServletRequest, resp: HttpServletResponse) {
        val users = userService.getAllUsers()
        
        // 使用 Java Stream API
        val activeUsers = users.stream()
            .filter { it.isActive }
            .map { it.toJson() }
            .collect(Collectors.toList())
        
        resp.contentType = "application/json"
        resp.writer.write(gson.toJson(activeUsers))
    }
}

// ===== 11. 主函数和程序入口 =====

fun main(args: Array<string>) {
    println("🚀 Welcome to Starlight!")
    
    // 创建测试数据
    val users = listOf(
        User("Alice", 25, "alice@example.com"),
        User("Bob", 17, null),
        User("Charlie", 67, "charlie@example.com")
    )
    
    val products = listOf(
        Product(1, "Laptop", 999.99, "Electronics"),
        Product(2, "Book", 19.99, "Books"),
        Product(3, "Phone", 699.99, "Electronics")
    )
    
    // 应用规则
    users.forEach { user ->
        if (user.age >= 18) user.canVote = true
        if (user.age >= 65) user.discount = 0.15
    }
    
    // 使用扩展函数
    val emailUsers = users.filter { it.email?.isEmail() == true }
    println("Users with valid email: ${emailUsers.size}")
    
    // 使用列表推导式
    val adultNames = [user.name | for user in users if user.isAdult()]
    println("Adult users: ${adultNames.joinToString(", ")}")
    
    // 使用管道操作
    val expensiveElectronics = products
        | filter { it.category == "Electronics" }
        | filter { it.isExpensive() }
        | map { it.name }
    
    println("Expensive electronics: ${expensiveElectronics.joinToString(", ")}")
    
    // 异步操作示例
    async {
        val profile = await fetchUserProfile(1)
        println("Fetched profile: ${profile.user.name}")
    }
    
    // 事务示例
    val account1 = Account(1, 1000.0)
    val account2 = Account(2, 500.0)
    
    val success = transferMoney(account1, account2, 200.0)
    println("Transfer successful: ${success}")
    println("Account 1 balance: ${account1.balance}")
    println("Account 2 balance: ${account2.balance}")
    
    println("✨ Starlight demo completed!")
}

// ===== 12. 辅助类型定义 =====

enum UserAction {
    Login(username: string, password: string)
    Logout(userId: int)
    Purchase(userId: int, productId: int, quantity: int)
    Search(query: string, filters: Map<string, any>)
}

data UserProfile(
    user: User,
    preferences: UserPreferences,
    purchaseHistory: List<Purchase>
)

data Account(id: int, var balance: float)
data Transaction(fromAccountId: int, toAccountId: int, amount: float)
data UserPreferences(theme: string, language: string, notifications: boolean)
data Purchase(productId: int, quantity: int, price: float, date: LocalDateTime)
