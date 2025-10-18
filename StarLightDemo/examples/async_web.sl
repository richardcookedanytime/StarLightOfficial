// Starlight 语言 - 异步编程和 Web API 示例
// 展示前后端统一的异步编程模式

// HTTP 客户端接口
interface HttpClient {
    func get(url: string) -> Promise<Response>
    func post(url: string, data: any) -> Promise<Response>
    func put(url: string, data: any) -> Promise<Response>
    func delete(url: string) -> Promise<Response>
}

// 响应类型
struct Response {
    status: int
    headers: Map<string, string>
    body: string
    ok: bool
}

// 用户 API 服务
struct UserService {
    httpClient: HttpClient
    baseUrl: string
}

// 用户结构体
struct User {
    id: int
    name: string
    email: string
    createdAt: string
}

// 用户服务方法
func UserService.getUsers() -> Promise<[User]> {
    try {
        let response = await this.httpClient.get("${this.baseUrl}/users");
        if response.ok {
            return JSON.parse(response.body);
        } else {
            throw Error("Failed to fetch users: ${response.status}");
        }
    } catch (error) {
        throw Error("Network error: ${error.message}");
    }
}

func UserService.createUser(user: User) -> Promise<User> {
    try {
        let response = await this.httpClient.post("${this.baseUrl}/users", user);
        if response.ok {
            return JSON.parse(response.body);
        } else {
            throw Error("Failed to create user: ${response.status}");
        }
    } catch (error) {
        throw Error("Network error: ${error.message}");
    }
}

// 并发处理多个请求
func UserService.getUsersAndStats() -> Promise<{users: [User], stats: any}> {
    // 并发执行多个异步操作
    let [users, stats] = await Promise.all([
        this.getUsers(),
        this.httpClient.get("${this.baseUrl}/stats").then(response => JSON.parse(response.body))
    ]);
    
    return {users, stats};
}

// Web 前端使用示例
func setupUserInterface() {
    let userService = UserService{
        httpClient: new FetchClient(),  // 浏览器 Fetch API 实现
        baseUrl: "/api"
    };
    
    // 加载用户数据
    async func loadUsers() {
        try {
            let data = await userService.getUsersAndStats();
            updateUserList(data.users);
            updateStats(data.stats);
        } catch (error) {
            showError("Failed to load data: ${error.message}");
        }
    }
    
    // 创建新用户
    async func createUser(userData: User) {
        try {
            let newUser = await userService.createUser(userData);
            addUserToList(newUser);
            showSuccess("User created successfully!");
        } catch (error) {
            showError("Failed to create user: ${error.message}");
        }
    }
    
    // 绑定事件监听器
    document.getElementById("loadBtn").addEventListener("click", loadUsers);
    document.getElementById("createBtn").addEventListener("click", () => {
        let formData = getFormData();
        createUser(formData);
    });
}

// Node.js 后端使用示例
func setupApiServer() {
    let userService = UserService{
        httpClient: new NodeHttpClient(),  // Node.js HTTP 实现
        baseUrl: "http://database-api:3000"
    };
    
    // Express.js 风格的路由
    let server = new HttpServer();
    
    server.get("/api/users", async (req, res) => {
        try {
            let users = await userService.getUsers();
            res.json(users);
        } catch (error) {
            res.status(500).json({error: error.message});
        }
    });
    
    server.post("/api/users", async (req, res) => {
        try {
            let user = req.json<User>();
            let newUser = await userService.createUser(user);
            res.status(201).json(newUser);
        } catch (error) {
            res.status(400).json({error: error.message});
        }
    });
    
    server.listen(8080, () => {
        console.log("Server running on port 8080");
    });
}

// 启动应用
if (typeof window !== "undefined") {
    // 浏览器环境
    setupUserInterface();
} else {
    // Node.js 环境
    setupApiServer();
}
