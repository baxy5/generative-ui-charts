import { X } from "lucide-react";
import React from "react";

interface SystemMessageProps {
  message: string | null;
  setMessage: (message: string) => void;
}

const SystemMessage = ({ message, setMessage }: SystemMessageProps) => {
  return (
    message && (
      <div
        onClick={() => setMessage("")}
        className="relative w-full max-w-5xl mx-auto mt-4 mb-4 p-3 bg-red-900 text-white rounded-lg shadow-md transition-all duration-150 ease-in-out cursor-pointer hover:scale-[100.5%]"
      >
        {message}

        <div className="absolute top-1 right-1 cursor-pointer">
          <X size={20} />
        </div>
      </div>
    )
  );
};

export default SystemMessage;
