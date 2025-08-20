import { useState, useRef, useEffect } from "react";
import { queryBackend } from "./api";
import ReactMarkdown from "react-markdown";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await queryBackend(input);
      const botMsg = { role: "assistant", text: data.answer || "No response." };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 w-full max-w-2xl">
      <div
        className={`flex flex-col bg-gray-900 rounded-2xl shadow-lg transition-all duration-300
        ${messages.length === 0 ? "h-16" : "h-[80vh]"}`}
      >
        {/* Messages Area */}
        {messages.length > 0 && (
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`px-4 py-2 rounded-2xl max-w-[75%] whitespace-pre-line shadow ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-black text-gray-200"
                  }`}
                >
                  {msg.role === "assistant" ? (
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  ) : (
                    msg.text
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <p className="italic text-gray-400">Thinking...</p>
            )}
            <div ref={bottomRef} />
          </div>
        )}

        {/* Input Box (hidden while loading) */}
        {!loading && (
          <form
            onSubmit={handleSubmit}
            className="p-3 flex gap-2 border-t border-gray-700"
          >
            <textarea
              className="flex-1 border rounded-lg px-3 py-2 resize-none bg-black text-white focus:outline-none"
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="submit"
              className="bg-blue-600 text-black px-4 rounded-lg hover:bg-blue-700"
            >
              Send
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
