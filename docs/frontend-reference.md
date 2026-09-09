# Guía de Referencia Frontend: React + TypeScript (Chat IA)

Este documento sirve como hoja de ruta y referencia rápida para estructurar y construir la interfaz de usuario de un Chat de IA utilizando **React** y **TypeScript**.

---

## 1. Stack Tecnológico Recomendado

* **Herramienta de Construcción:** Vite (`npm create vite@latest frontend -- --template react-ts`)
* **Estilos & UI:** Tailwind CSS v4 (`@tailwindcss/vite`) + Lucide Icons (`npm i lucide-react`)
* **Gestión de Peticiones / Streaming:** `fetch` con `ReadableStream` para respuestas en tiempo real (Server-Sent Events) o **TanStack Query** para peticiones HTTP estándar.

---

## 2. Definición de Tipos (`src/types/chat.ts`)

Definir los contratos de datos antes de crear los componentes garantiza la seguridad de tipos en toda la aplicación.

```typescript
export type Role = 'user' | 'assistant' | 'system';

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  messages: Pick<Message, 'role' | 'content'>[];
  temperature?: number;
}

export interface ChatResponse {
  id: string;
  message: Message;
}
```

---

## 3. Componente de Visualización de Mensajes (`src/components/MessageItem.tsx`)

Manejo de props con tipos e interfaces en TypeScript:

```tsx
import React from 'react';
import { Message } from '../types/chat';

interface MessageItemProps {
  message: Message;
  isLast?: boolean;
}

export const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div
        className={`max-w-[80%] p-3 rounded-lg ${
          isUser ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-100'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <span className="text-[10px] opacity-70 block text-right mt-1">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
};
```

---

## 4. Componente de Entrada de Texto (`src/components/ChatInput.tsx`)

Manejo correcto de eventos del DOM (`React.FormEvent` y `React.ChangeEvent`):

```tsx
import React, { useState } from 'react';

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t border-gray-700 bg-gray-800">
      <input
        type="text"
        value={input}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
        placeholder="Escribe tu mensaje..."
        disabled={isLoading}
        className="flex-1 p-2 bg-gray-900 border border-gray-700 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="px-4 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-500 disabled:opacity-50 transition-colors"
      >
        {isLoading ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  );
};
```

---

## 5. Próximos Pasos Siguientes

1. **Crear Custom Hook (`useChat`):**
   * Gestionar la lista de mensajes (`Message[]`).
   * Manejar los estados `isLoading` y `error`.
   * Integrar la llamada a tu API con soporte para Streaming (`ReadableStream`).

2. **Auto-scroll:**
   * Utilizar `useRef<HTMLDivElement>(null)` con `element.scrollIntoView({ behavior: 'smooth' })` para mantener la vista al final del chat tras cada respuesta.

3. **Revisión y Feedback:**
   * Cuando tengas implementada tu versión inicial, comparte tu código para revisar tipado, rendimiento y buenas prácticas en React.
