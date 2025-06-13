import { Loader, Plus, Send } from "lucide-react";
import React, { useRef } from "react";

interface ChatProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  dataset: File | null;
  setDataset: (dataset: File | null) => void;
  handleSubmit: () => void;
  isLoading: boolean;
}

const Chat = ({
  prompt,
  setPrompt,
  dataset,
  setDataset,
  handleSubmit,
  isLoading,
}: ChatProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      // Only submit if prompt is not empty (after trimming whitespace)
      if (prompt.trim()) {
        handleSubmit();
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) setDataset(e.target.files[0]);
  };

  const handlePlusClick = () => {
    fileInputRef.current?.click();
  };

  const onRemove = () => {
    setDataset(null);
  };

  return (
    <div className="max-w-5xl mx-auto bg-gray-800 rounded-lg shadow-md mt-4 p-4">
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
        {!dataset ? (
          <>
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.json"
            />
            <button
              className="cursor-pointer hover:scale-110"
              onClick={handlePlusClick}
            >
              <Plus />
            </button>
          </>
        ) : (
          <div>
            <p className="font-bold text-[#13856c]">{dataset.name}</p>
            <span
              className="text-gray-500 text-[10px] uppercase font-bold cursor-pointer hover:text-gray-400"
              onClick={onRemove}
            >
              remove
            </span>
          </div>
        )}
        <button
          onClick={handleSubmit}
          disabled={(!prompt.trim() && !dataset) || isLoading}
          className={`p-2 bg-[#13856ce7] text-white rounded-lg
                ${
                  prompt.trim() && dataset && !isLoading
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
