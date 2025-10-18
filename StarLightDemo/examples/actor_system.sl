// Starlight 语言 - Actor 模型示例
// 展示并发和分布式编程

// 计数器 Actor
actor Counter {
    count: int = 0
    
    receive Increment(amount: int) {
        this.count += amount;
        reply(this.count);
    }
    
    receive Decrement(amount: int) {
        this.count -= amount;
        reply(this.count);
    }
    
    receive Get() {
        reply(this.count);
    }
    
    receive Reset() {
        this.count = 0;
        reply("Counter reset");
    }
}

// 消息队列 Actor
actor MessageQueue {
    messages: [string] = []
    subscribers: [Actor] = []
    
    receive Send(message: string) {
        this.messages.push(message);
        
        // 通知所有订阅者
        for (subscriber in this.subscribers) {
            subscriber.send(NewMessage(message));
        }
        
        reply("Message sent");
    }
    
    receive Subscribe(subscriber: Actor) {
        this.subscribers.push(subscriber);
        reply("Subscribed");
    }
    
    receive GetMessages() {
        reply(this.messages);
    }
}

// 聊天室 Actor
actor ChatRoom {
    name: string
    participants: Map<string, Actor> = {}
    messageQueue: Actor
    
    receive Join(userId: string, userActor: Actor) {
        this.participants.set(userId, userActor);
        this.messageQueue.send(Subscribe(userActor));
        reply("Joined ${this.name}");
    }
    
    receive Leave(userId: string) {
        this.participants.delete(userId);
        reply("Left ${this.name}");
    }
    
    receive Broadcast(userId: string, message: string) {
        let broadcastMessage = "${userId}: ${message}";
        this.messageQueue.send(Send(broadcastMessage));
        reply("Message broadcasted");
    }
    
    receive GetParticipants() {
        let userIds = this.participants.keys();
        reply(userIds);
    }
}

// 用户 Actor
actor User {
    userId: string
    chatRooms: [Actor] = []
    
    receive JoinRoom(room: Actor) {
        let result = await room.send(Join(this.userId, this));
        this.chatRooms.push(room);
        reply(result);
    }
    
    receive LeaveRoom(room: Actor) {
        let result = await room.send(Leave(this.userId));
        this.chatRooms = this.chatRooms.filter(r => r !== room);
        reply(result);
    }
    
    receive SendMessage(room: Actor, message: string) {
        let result = await room.send(Broadcast(this.userId, message));
        reply(result);
    }
    
    receive NewMessage(message: string) {
        console.log("${this.userId} received: ${message}");
        reply("Message received");
    }
    
    receive GetChatRooms() {
        reply(this.chatRooms.length);
    }
}

// 分布式系统协调器
actor SystemCoordinator {
    counters: [Actor] = []
    chatRooms: [Actor] = []
    users: [Actor] = []
    
    receive CreateCounter() -> Actor {
        let counter = spawn Counter();
        this.counters.push(counter);
        reply(counter);
    }
    
    receive CreateChatRoom(name: string) -> Actor {
        let messageQueue = spawn MessageQueue();
        let chatRoom = spawn ChatRoom(name, messageQueue);
        this.chatRooms.push(chatRoom);
        reply(chatRoom);
    }
    
    receive CreateUser(userId: string) -> Actor {
        let user = spawn User(userId);
        this.users.push(user);
        reply(user);
    }
    
    receive GetSystemStats() {
        let stats = {
            counters: this.counters.length,
            chatRooms: this.chatRooms.length,
            users: this.users.length
        };
        reply(stats);
    }
}

// 使用示例
func demonstrateActorSystem() {
    // 创建系统协调器
    let coordinator = spawn SystemCoordinator();
    
    // 创建用户
    let alice = await coordinator.send(CreateUser("alice"));
    let bob = await coordinator.send(CreateUser("bob"));
    let charlie = await coordinator.send(CreateUser("charlie"));
    
    // 创建聊天室
    let generalRoom = await coordinator.send(CreateChatRoom("general"));
    let techRoom = await coordinator.send(CreateChatRoom("tech"));
    
    // 用户加入聊天室
    await alice.send(JoinRoom(generalRoom));
    await bob.send(JoinRoom(generalRoom));
    await charlie.send(JoinRoom(techRoom));
    await alice.send(JoinRoom(techRoom));
    
    // 发送消息
    await alice.send(SendMessage(generalRoom, "Hello everyone!"));
    await bob.send(SendMessage(generalRoom, "Hi Alice!"));
    await charlie.send(SendMessage(techRoom, "Any Python developers here?"));
    await alice.send(SendMessage(techRoom, "I work with Python!"));
    
    // 演示计数器
    let counter1 = await coordinator.send(CreateCounter());
    let counter2 = await coordinator.send(CreateCounter());
    
    // 并发操作计数器
    let [count1, count2] = await Promise.all([
        counter1.send(Increment(10)),
        counter2.send(Increment(20))
    ]);
    
    console.log("Counter 1: ${count1}");
    console.log("Counter 2: ${count2}");
    
    // 获取系统统计
    let stats = await coordinator.send(GetSystemStats());
    console.log("System stats: ${stats}");
}

// 启动演示
demonstrateActorSystem();
