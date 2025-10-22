// 运算符重载示例

// 向量类，支持运算符重载
data Vector(x: float, y: float) {
    // 重载 + 运算符
    operator fun plus(other: Vector): Vector {
        return Vector(x + other.x, y + other.y)
    }
    
    // 重载 - 运算符
    operator fun minus(other: Vector): Vector {
        return Vector(x - other.x, y - other.y)
    }
    
    // 重载 * 运算符 (标量乘法)
    operator fun times(scalar: float): Vector {
        return Vector(x * scalar, y * scalar)
    }
    
    // 重载 == 运算符
    operator fun equals(other: Vector): boolean {
        return x == other.x && y == other.y
    }
    
    fun toString(): string {
        return "Vector(${x}, ${y})"
    }
}

fun main() {
    let v1 = Vector(1.0, 2.0)
    let v2 = Vector(3.0, 4.0)
    
    // 使用重载的运算符
    let sum = v1 + v2
    println("v1 + v2 = " + sum.toString())
    
    let diff = v2 - v1
    println("v2 - v1 = " + diff.toString())
    
    let scaled = v1 * 2.0
    println("v1 * 2 = " + scaled.toString())
    
    // 比较
    let isEqual = v1 == v2
    println("v1 == v2: " + isEqual)
}

