import React, { useState } from 'react';
import { chatWithResume } from '../api';

export const ChatInterface: React.FC = () => {
    const [messages, setMessages] = useState<{ role: 'user' | 'ai', content: string }[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setInput("");
        setLoading(true);

        try {
            const res = await chatWithResume(userMsg);
            setMessages(prev => [...prev, { role: 'ai', content: res.answer }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'ai', content: "Error getting response." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto mt-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Chat with Resume</h2>
            <div className="border rounded-lg h-64 overflow-y-auto p-4 mb-4 bg-gray-50">
                {messages.length === 0 && <p className="text-gray-400 text-center mt-20">Ask questions like "Does he have React experience?"</p>}
                {messages.map((m, i) => (
                    <div key={i} className={`mb-3 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block px-3 py-2 rounded-lg text-sm ${m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}`}>
                            {m.content}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-center text-xs text-gray-400">AI is thinking...</div>}
            </div>
            <form onSubmit={handleSend} className="flex">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about the candidate..."
                    className="flex-1 border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white px-6 rounded-r-lg hover:bg-blue-700 disabled:opacity-50"
                >
                    Send
                </button>
            </form>
        </div>
    );
};
