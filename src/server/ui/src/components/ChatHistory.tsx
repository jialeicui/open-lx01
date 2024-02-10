import Message from "@/components/Message";

export interface MessageItem {
    message: string
    timestamp: number
    role: 'user' | 'assistant'
}

export interface ChatHistoryProps {
    messages: MessageItem[]
}

export default function ChatHistory({messages}: ChatHistoryProps) {
    return (
        <div>
            {messages.map((message, index) => (
                <Message message={message.message} avatar={message.role === 'user' ? '👤' : '🤖'} key={index}
                         role={message.role}/>
            ))}
        </div>
    )
}

