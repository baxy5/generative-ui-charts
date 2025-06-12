import { Loader, Plus, Send } from "lucide-react";
import React from "react";

interface ChatProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  handleSubmit: () => void;
  isLoading: boolean;
}

const Chat = ({ prompt, setPrompt, handleSubmit, isLoading }: ChatProps) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      // Only submit if prompt is not empty (after trimming whitespace)
      if (prompt.trim()) {
        handleSubmit();
      }
    }
  };

  return (
    <div className="max-w-5xl mx-auto bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex items-center">
        <textarea
          placeholder="Ask anything"
          className="flex-grow p-2 rounded-lg bg-gray-700 text-white focus:outline-none min-h-[40px] max-h-[200px] resize-none"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
        />
      </div>
      <div className="flex items-center justify-between pt-4">
        <Plus />
        <button
          onClick={handleSubmit}
          disabled={!prompt.trim() || isLoading}
          className={`p-2 bg-[#13856ce7] text-white rounded-lg
                ${
                  prompt.trim() && !isLoading
                    ? "opacity-100 hover:bg-[#13856c] focus:outline-none cursor-pointer"
                    : "opacity-50 cursor-not-allowed"
                }`}
        >
          {!isLoading && <Send size={16} />}
          {isLoading && <Loader size={16} className="animate-spin" />}
        </button>
      </div>
    </div>
  );
};

export default Chat;
