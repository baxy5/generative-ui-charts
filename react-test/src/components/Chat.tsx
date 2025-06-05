import { Loader, Plus, Send } from "lucide-react";
import React from "react";

interface ChatProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  handleSubmit: () => void;
  isLoading: boolean;
}

const Chat = ({ prompt, setPrompt, handleSubmit, isLoading }: ChatProps) => {
  return (
    <div className="max-w-md mx-auto bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex items-center">
        <textarea
          placeholder="Ask anything"
          className="flex-grow p-2 rounded-lg bg-gray-700 text-white focus:outline-none min-h-[40px] max-h-[200px] resize-none"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={3}
        />
      </div>
      <div className="flex items-center justify-between pt-4">
        <Plus />
        <button
          onClick={handleSubmit}
          className={`p-2 bg-blue-800 text-white rounded-lg
                ${
                  prompt
                    ? "opacity-100 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-700 cursor-pointer"
                    : "opacity-50"
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
