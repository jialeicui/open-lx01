import * as React from 'react'
import Container from '@mui/material/Container'
import ChatHistory, { MessageItem } from '@/components/ChatHistory'

export default function Home() {
  const messages: MessageItem[] = [
    { message: 'Hello', timestamp: 123, role: 'user' },
    { message: 'Hello from bot', timestamp: 123, role: 'assistant' },
  ]
  return (
    <Container maxWidth='lg'>
      <ChatHistory messages={messages} />
    </Container>
  )
}
