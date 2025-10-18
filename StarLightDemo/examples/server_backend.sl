// Starlight 语言 - 服务器后端示例
// 展示 RESTful API 和数据库操作

// 导入必要的模块
import { Database, HttpServer, Router, Middleware } from "starlight/std";

// 数据库模型
struct User {
    id: int
    username: string
    email: string
    passwordHash: string
    createdAt: string
    updatedAt: string
}

struct Post {
    id: int
    title: string
    content: string
    authorId: int
    published: bool
    createdAt: string
    updatedAt: string
}

struct Comment {
    id: int
    postId: int
    authorId: int
    content: string
    createdAt: string
}

// 服务层
class UserService {
    db: Database
    
    constructor(database: Database) {
        this.db = database;
    }
    
    async createUser(userData: {username: string, email: string, password: string}): Promise<User> {
        let passwordHash = await this.hashPassword(userData.password);
        
        let user = User{
            id: 0, // 数据库自动生成
            username: userData.username,
            email: userData.email,
            passwordHash: passwordHash,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        let result = await this.db.query(`
            INSERT INTO users (username, email, password_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            RETURNING *
        `, [user.username, user.email, user.passwordHash, user.createdAt, user.updatedAt]);
        
        return result[0] as User;
    }
    
    async getUserById(id: int): Promise<User | null> {
        let result = await this.db.query("SELECT * FROM users WHERE id = ?", [id]);
        return result.length > 0 ? result[0] as User : null;
    }
    
    async getUserByEmail(email: string): Promise<User | null> {
        let result = await this.db.query("SELECT * FROM users WHERE email = ?", [email]);
        return result.length > 0 ? result[0] as User : null;
    }
    
    async updateUser(id: int, updates: Partial<User>): Promise<User | null> {
        let setClause = [];
        let values = [];
        
        if (updates.username) {
            setClause.push("username = ?");
            values.push(updates.username);
        }
        if (updates.email) {
            setClause.push("email = ?");
            values.push(updates.email);
        }
        
        setClause.push("updated_at = ?");
        values.push(new Date().toISOString());
        values.push(id);
        
        let query = `UPDATE users SET ${setClause.join(", ")} WHERE id = ? RETURNING *`;
        let result = await this.db.query(query, values);
        
        return result.length > 0 ? result[0] as User : null;
    }
    
    async deleteUser(id: int): Promise<boolean> {
        let result = await this.db.query("DELETE FROM users WHERE id = ?", [id]);
        return result.affectedRows > 0;
    }
    
    async verifyPassword(password: string, hash: string): Promise<boolean> {
        return await bcrypt.compare(password, hash);
    }
    
    async hashPassword(password: string): Promise<string> {
        return await bcrypt.hash(password, 12);
    }
}

class PostService {
    db: Database
    
    constructor(database: Database) {
        this.db = database;
    }
    
    async createPost(postData: {title: string, content: string, authorId: int}): Promise<Post> {
        let post = Post{
            id: 0,
            title: postData.title,
            content: postData.content,
            authorId: postData.authorId,
            published: false,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        let result = await this.db.query(`
            INSERT INTO posts (title, content, author_id, published, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            RETURNING *
        `, [post.title, post.content, post.authorId, post.published, post.createdAt, post.updatedAt]);
        
        return result[0] as Post;
    }
    
    async getPosts(page: int = 1, limit: int = 10, publishedOnly: bool = true): Promise<[Post]> {
        let offset = (page - 1) * limit;
        let whereClause = publishedOnly ? "WHERE published = true" : "";
        
        let result = await this.db.query(`
            SELECT p.*, u.username as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            ${whereClause}
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
        `, [limit, offset]);
        
        return result;
    }
    
    async getPostById(id: int): Promise<Post | null> {
        let result = await this.db.query(`
            SELECT p.*, u.username as author_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.id = ?
        `, [id]);
        
        return result.length > 0 ? result[0] as Post : null;
    }
    
    async updatePost(id: int, updates: Partial<Post>): Promise<Post | null> {
        let setClause = [];
        let values = [];
        
        if (updates.title) {
            setClause.push("title = ?");
            values.push(updates.title);
        }
        if (updates.content) {
            setClause.push("content = ?");
            values.push(updates.content);
        }
        if (updates.published !== null) {
            setClause.push("published = ?");
            values.push(updates.published);
        }
        
        setClause.push("updated_at = ?");
        values.push(new Date().toISOString());
        values.push(id);
        
        let query = `UPDATE posts SET ${setClause.join(", ")} WHERE id = ? RETURNING *`;
        let result = await this.db.query(query, values);
        
        return result.length > 0 ? result[0] as Post : null;
    }
    
    async deletePost(id: int): Promise<boolean> {
        // 先删除相关评论
        await this.db.query("DELETE FROM comments WHERE post_id = ?", [id]);
        
        // 删除文章
        let result = await this.db.query("DELETE FROM posts WHERE id = ?", [id]);
        return result.affectedRows > 0;
    }
}

// 中间件
class AuthMiddleware implements Middleware {
    userService: UserService
    
    constructor(userService: UserService) {
        this.userService = userService;
    }
    
    async handle(req: Request, res: Response, next: () -> Promise<void>): Promise<void> {
        let token = req.headers.authorization?.replace("Bearer ", "");
        
        if (!token) {
            res.status(401).json({error: "No authentication token provided"});
            return;
        }
        
        try {
            let payload = jwt.verify(token, process.env.JWT_SECRET);
            let user = await this.userService.getUserById(payload.userId);
            
            if (!user) {
                res.status(401).json({error: "Invalid token"});
                return;
            }
            
            req.user = user;
            await next();
        } catch (error) {
            res.status(401).json({error: "Invalid token"});
        }
    }
}

class ValidationMiddleware implements Middleware {
    schema: any
    
    constructor(schema: any) {
        this.schema = schema;
    }
    
    async handle(req: Request, res: Response, next: () -> Promise<void>): Promise<void> {
        try {
            let validation = this.schema.validate(req.body);
            
            if (!validation.valid) {
                res.status(400).json({
                    error: "Validation failed",
                    details: validation.errors
                });
                return;
            }
            
            req.validatedData = validation.data;
            await next();
        } catch (error) {
            res.status(400).json({error: "Invalid request data"});
        }
    }
}

// 控制器
class AuthController {
    userService: UserService
    
    constructor(userService: UserService) {
        this.userService = userService;
    }
    
    async register(req: Request, res: Response): Promise<void> {
        try {
            let {username, email, password} = req.validatedData;
            
            // 检查用户是否已存在
            let existingUser = await this.userService.getUserByEmail(email);
            if (existingUser) {
                res.status(409).json({error: "User already exists"});
                return;
            }
            
            let user = await this.userService.createUser({username, email, password});
            
            // 生成 JWT token
            let token = jwt.sign({userId: user.id}, process.env.JWT_SECRET, {expiresIn: "7d"});
            
            res.status(201).json({
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email
                },
                token: token
            });
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
    
    async login(req: Request, res: Response): Promise<void> {
        try {
            let {email, password} = req.validatedData;
            
            let user = await this.userService.getUserByEmail(email);
            if (!user) {
                res.status(401).json({error: "Invalid credentials"});
                return;
            }
            
            let isValidPassword = await this.userService.verifyPassword(password, user.passwordHash);
            if (!isValidPassword) {
                res.status(401).json({error: "Invalid credentials"});
                return;
            }
            
            let token = jwt.sign({userId: user.id}, process.env.JWT_SECRET, {expiresIn: "7d"});
            
            res.json({
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email
                },
                token: token
            });
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
}

class PostController {
    postService: PostService
    
    constructor(postService: PostService) {
        this.postService = postService;
    }
    
    async getPosts(req: Request, res: Response): Promise<void> {
        try {
            let page = parseInt(req.query.page || "1");
            let limit = parseInt(req.query.limit || "10");
            let publishedOnly = req.query.published !== "false";
            
            let posts = await this.postService.getPosts(page, limit, publishedOnly);
            
            res.json({
                posts: posts,
                pagination: {
                    page: page,
                    limit: limit,
                    total: posts.length
                }
            });
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
    
    async getPost(req: Request, res: Response): Promise<void> {
        try {
            let id = parseInt(req.params.id);
            let post = await this.postService.getPostById(id);
            
            if (!post) {
                res.status(404).json({error: "Post not found"});
                return;
            }
            
            res.json({post: post});
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
    
    async createPost(req: Request, res: Response): Promise<void> {
        try {
            let {title, content} = req.validatedData;
            let authorId = req.user.id;
            
            let post = await this.postService.createPost({title, content, authorId});
            
            res.status(201).json({post: post});
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
    
    async updatePost(req: Request, res: Response): Promise<void> {
        try {
            let id = parseInt(req.params.id);
            let updates = req.validatedData;
            
            let post = await this.postService.updatePost(id, updates);
            
            if (!post) {
                res.status(404).json({error: "Post not found"});
                return;
            }
            
            res.json({post: post});
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
    
    async deletePost(req: Request, res: Response): Promise<void> {
        try {
            let id = parseInt(req.params.id);
            let success = await this.postService.deletePost(id);
            
            if (!success) {
                res.status(404).json({error: "Post not found"});
                return;
            }
            
            res.status(204).send();
        } catch (error) {
            res.status(500).json({error: "Internal server error"});
        }
    }
}

// 应用设置
func setupApp(): HttpServer {
    // 数据库连接
    let db = new Database({
        host: process.env.DB_HOST || "localhost",
        port: parseInt(process.env.DB_PORT || "5432"),
        database: process.env.DB_NAME || "starlight_app",
        username: process.env.DB_USER || "postgres",
        password: process.env.DB_PASSWORD || "password"
    });
    
    // 服务初始化
    let userService = new UserService(db);
    let postService = new PostService(db);
    
    // 控制器初始化
    let authController = new AuthController(userService);
    let postController = new PostController(postService);
    
    // 中间件
    let authMiddleware = new AuthMiddleware(userService);
    
    let userSchema = {
        username: {type: "string", required: true, minLength: 3},
        email: {type: "string", required: true, format: "email"},
        password: {type: "string", required: true, minLength: 6}
    };
    
    let loginSchema = {
        email: {type: "string", required: true, format: "email"},
        password: {type: "string", required: true}
    };
    
    let postSchema = {
        title: {type: "string", required: true, minLength: 1},
        content: {type: "string", required: true, minLength: 1}
    };
    
    let userValidation = new ValidationMiddleware(userSchema);
    let loginValidation = new ValidationMiddleware(loginSchema);
    let postValidation = new ValidationMiddleware(postSchema);
    
    // 路由设置
    let router = new Router();
    
    // 认证路由
    router.post("/api/auth/register", userValidation, authController.register);
    router.post("/api/auth/login", loginValidation, authController.login);
    
    // 文章路由
    router.get("/api/posts", postController.getPosts);
    router.get("/api/posts/:id", postController.getPost);
    router.post("/api/posts", authMiddleware, postValidation, postController.createPost);
    router.put("/api/posts/:id", authMiddleware, postValidation, postController.updatePost);
    router.delete("/api/posts/:id", authMiddleware, postController.deletePost);
    
    // 创建服务器
    let server = new HttpServer();
    server.use(router);
    
    // 错误处理中间件
    server.use((req: Request, res: Response, next: () -> Promise<void>) => {
        res.status(404).json({error: "Route not found"});
    });
    
    return server;
}

// 启动应用
func main() {
    let server = setupApp();
    let port = parseInt(process.env.PORT || "3000");
    
    server.listen(port, () => {
        console.log(`Server running on port ${port}`);
        console.log(`Environment: ${process.env.NODE_ENV || "development"}`);
    });
}

// 优雅关闭
process.on("SIGTERM", () => {
    console.log("Received SIGTERM, shutting down gracefully...");
    process.exit(0);
});

process.on("SIGINT", () => {
    console.log("Received SIGINT, shutting down gracefully...");
    process.exit(0);
});

// 启动应用
main();
