import React from "react";
import SystemMessage from "./SystemMessage";
import Chat from "./Chat";
import { ChatProps } from "./Chat";
import { SystemMessageProps } from "./SystemMessage";

interface ChatContainerProps extends ChatProps, SystemMessageProps {}

const ChatContainer = ({
  prompt,
  setPrompt,
  dataset,
  setDataset,
  handleSubmit,
  isLoading,
  message,
  setMessage,
}: ChatContainerProps) => {
  return (
    <div className="row-start-6 w-full">
      <SystemMessage message={message} setMessage={setMessage} />
      <Chat
        prompt={prompt}
        setPrompt={setPrompt}
        dataset={dataset}
        setDataset={setDataset}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </div>
  );
};

export default ChatContainer;
