// Starlight 语言 - Web 前端示例
// 展示现代 Web 开发特性

// 组件系统
interface Component {
    func render(): HTMLElement
    func mount(container: HTMLElement): void
    func unmount(): void
}

// 状态管理
class State<T> {
    value: T
    subscribers: [(T) -> void] = []
    
    constructor(initialValue: T) {
        this.value = initialValue;
    }
    
    get(): T {
        return this.value;
    }
    
    set(newValue: T) {
        this.value = newValue;
        this.notifySubscribers();
    }
    
    subscribe(callback: (T) -> void) {
        this.subscribers.push(callback);
    }
    
    notifySubscribers() {
        for (callback in this.subscribers) {
            callback(this.value);
        }
    }
}

// Todo 项目类型
struct TodoItem {
    id: string
    text: string
    completed: bool
    createdAt: string
}

// Todo 应用状态
struct TodoState {
    todos: [TodoItem]
    filter: "all" | "active" | "completed"
    newTodoText: string
}

// Todo 应用组件
class TodoApp implements Component {
    state: State<TodoState>
    container: HTMLElement | null = null
    
    constructor() {
        this.state = new State(TodoState{
            todos: [],
            filter: "all",
            newTodoText: ""
        });
    }
    
    render(): HTMLElement {
        let div = document.createElement("div");
        div.className = "todo-app";
        
        div.innerHTML = `
            <div class="header">
                <h1>Starlight Todo App</h1>
                <div class="input-group">
                    <input 
                        type="text" 
                        id="newTodo" 
                        placeholder="What needs to be done?"
                        value="${this.state.get().newTodoText}"
                    />
                    <button id="addTodo">Add</button>
                </div>
            </div>
            
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="active">Active</button>
                <button class="filter-btn" data-filter="completed">Completed</button>
            </div>
            
            <ul id="todoList" class="todo-list">
                ${this.renderTodoList()}
            </ul>
            
            <div class="footer">
                <span id="todoCount">0 items left</span>
                <button id="clearCompleted">Clear Completed</button>
            </div>
        `;
        
        this.bindEvents(div);
        return div;
    }
    
    renderTodoList(): string {
        let todos = this.getFilteredTodos();
        
        return todos.map(todo => `
            <li class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
                <input 
                    type="checkbox" 
                    class="todo-checkbox" 
                    ${todo.completed ? 'checked' : ''}
                />
                <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                <button class="delete-btn">×</button>
            </li>
        `).join("");
    }
    
    getFilteredTodos(): [TodoItem] {
        let state = this.state.get();
        
        match state.filter {
            "active" => state.todos.filter(todo => !todo.completed)
            "completed" => state.todos.filter(todo => todo.completed)
            _ => state.todos
        }
    }
    
    bindEvents(container: HTMLElement) {
        // 添加新 Todo
        let addButton = container.querySelector("#addTodo");
        let newTodoInput = container.querySelector("#newTodo") as HTMLInputElement;
        
        addButton?.addEventListener("click", () => this.addTodo());
        newTodoInput?.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                this.addTodo();
            }
        });
        
        // 过滤按钮
        let filterButtons = container.querySelectorAll(".filter-btn");
        filterButtons.forEach(btn => {
            btn.addEventListener("click", (e) => {
                let filter = (e.target as HTMLElement).dataset.filter;
                this.setFilter(filter);
            });
        });
        
        // Todo 列表事件委托
        let todoList = container.querySelector("#todoList");
        todoList?.addEventListener("click", (e) => {
            let target = e.target as HTMLElement;
            
            if (target.classList.contains("todo-checkbox")) {
                let todoId = target.closest(".todo-item")?.dataset.id;
                this.toggleTodo(todoId);
            } else if (target.classList.contains("delete-btn")) {
                let todoId = target.closest(".todo-item")?.dataset.id;
                this.deleteTodo(todoId);
            }
        });
        
        // 清除已完成
        let clearButton = container.querySelector("#clearCompleted");
        clearButton?.addEventListener("click", () => this.clearCompleted());
    }
    
    addTodo() {
        let state = this.state.get();
        let text = state.newTodoText.trim();
        
        if (text) {
            let newTodo = TodoItem{
                id: this.generateId(),
                text: text,
                completed: false,
                createdAt: new Date().toISOString()
            };
            
            this.state.set({
                ...state,
                todos: [...state.todos, newTodo],
                newTodoText: ""
            });
        }
    }
    
    toggleTodo(id: string | undefined) {
        if (!id) return;
        
        let state = this.state.get();
        let updatedTodos = state.todos.map(todo =>
            todo.id === id ? {...todo, completed: !todo.completed} : todo
        );
        
        this.state.set({...state, todos: updatedTodos});
    }
    
    deleteTodo(id: string | undefined) {
        if (!id) return;
        
        let state = this.state.get();
        let updatedTodos = state.todos.filter(todo => todo.id !== id);
        
        this.state.set({...state, todos: updatedTodos});
    }
    
    setFilter(filter: string | undefined) {
        if (!filter) return;
        
        let state = this.state.get();
        this.state.set({...state, filter});
        
        // 更新按钮状态
        document.querySelectorAll(".filter-btn").forEach(btn => {
            btn.classList.remove("active");
        });
        document.querySelector(`[data-filter="${filter}"]`)?.classList.add("active");
    }
    
    clearCompleted() {
        let state = this.state.get();
        let activeTodos = state.todos.filter(todo => !todo.completed);
        
        this.state.set({...state, todos: activeTodos});
    }
    
    mount(container: HTMLElement) {
        this.container = container;
        container.appendChild(this.render());
        
        // 监听状态变化，自动重新渲染
        this.state.subscribe(() => this.updateView());
    }
    
    unmount() {
        this.container?.remove();
        this.container = null;
    }
    
    updateView() {
        if (!this.container) return;
        
        let todoList = this.container.querySelector("#todoList");
        let todoCount = this.container.querySelector("#todoCount");
        let newTodoInput = this.container.querySelector("#newTodo") as HTMLInputElement;
        
        if (todoList) {
            todoList.innerHTML = this.renderTodoList();
        }
        
        if (todoCount) {
            let activeCount = this.state.get().todos.filter(todo => !todo.completed).length;
            todoCount.textContent = "${activeCount} items left";
        }
        
        if (newTodoInput) {
            newTodoInput.value = this.state.get().newTodoText;
        }
    }
    
    generateId(): string {
        return "todo_" + Math.random().toString(36).substr(2, 9);
    }
    
    escapeHtml(text: string): string {
        let div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
}

// 路由系统
class Router {
    routes: Map<string, () -> void> = {}
    currentPath: string = "/"
    
    addRoute(path: string, handler: () -> void) {
        this.routes.set(path, handler);
    }
    
    navigate(path: string) {
        if (this.routes.has(path)) {
            this.currentPath = path;
            history.pushState(null, "", path);
            this.routes.get(path)();
        }
    }
    
    start() {
        // 监听浏览器前进后退
        window.addEventListener("popstate", () => {
            this.navigate(window.location.pathname);
        });
        
        // 初始路由
        this.navigate(window.location.pathname);
    }
}

// 应用入口
func main() {
    // 创建路由
    let router = new Router();
    
    // 添加路由
    router.addRoute("/", () => {
        let container = document.getElementById("app");
        if (container) {
            container.innerHTML = "";
            let todoApp = new TodoApp();
            todoApp.mount(container);
        }
    });
    
    router.addRoute("/about", () => {
        let container = document.getElementById("app");
        if (container) {
            container.innerHTML = `
                <div class="about">
                    <h1>About Starlight</h1>
                    <p>Starlight is a modern programming language designed for high adaptability and universal use across frontend and backend development.</p>
                    <a href="/">← Back to Todos</a>
                </div>
            `;
        }
    });
    
    // 启动路由
    router.start();
}

// 页面加载完成后启动应用
document.addEventListener("DOMContentLoaded", main);
