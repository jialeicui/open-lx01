import { ReactNode } from 'react'

export interface MessageProps {
  message: string
  avatar: ReactNode
  role: string
}

export default function Message(props: MessageProps) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: props.role === 'user' ? 'row' : 'row-reverse',
        alignItems: 'center',
      }}
    >
      {props.avatar}
      <div
        style={{
          margin: '10px',
        }}
      >
        {props.message}
      </div>
    </div>
  )
}
