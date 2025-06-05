import React from "react";

interface SystemMessageProps {
  message: string | null;
}

const SystemMessage = ({ message }: SystemMessageProps) => {
  return (
    message && (
      <div className="max-w-md mx-auto mb-4 p-3 bg-red-900 text-white rounded-lg shadow-md">
        {message}
      </div>
    )
  );
};

export default SystemMessage;
