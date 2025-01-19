import { Search } from "lucide-react";
import { useFetch } from "@gadgetinc/react"; 
import { useState, useEffect, useRef } from "react";
import { useOutletContext } from "@remix-run/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input"; 
import { cn } from "@/lib/utils";
import { RootOutletContext } from "../root";
import { GradientCard } from "@/components/ui/gradient-card";
import { TextCard } from "@/components/ui/text-card";

export default function() {
  const { gadgetConfig } = useOutletContext<RootOutletContext>();
  interface Message {
    type: 'user' | 'ai';
    content: string;
  }
  const [searchInput, setSearchInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSecondInput, setSecondInput] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
 

  const [{ data, error, fetching }, sendFetch] = useFetch(
    "https://collectionapi.metmuseum.org/public/collection/v1/objects/436535",
    { json: true, sendImmediately: false });

  // Trigger API call when `submittedText` changes
  useEffect(() => {
    if (messages.length > 0 && messages[messages.length - 1].type === 'user') {
      void sendFetch();
    }
  }, [messages]);

  useEffect(() => {
    if (data && !fetching) {
      setMessages(prev => [...prev, {
        type: 'ai',
        content: `${data.title} by ${data.artistDisplayName}, ${data.objectDate}`
      }]);
    }
  }, [data, fetching]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
   
    
  const handleSearch = async () => {
    if (searchInput.trim()) {
      // Add the user message to chat
      setMessages(prev => [...prev, { type: 'user', content: searchInput.trim() }]);
      
      // Handle input sequence tracking
      if (isSecondInput) {
        setSecondInput(false);
        console.log('SECOND');
      }
      setSecondInput(!isSecondInput);
      setSearchInput("");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center bg-[#a6c6ff]">
      <div className={cn(
        "flex-1 w-1/2 p-6 border-none bg-[#ffaca6]",
      )}>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] bg-clip-text text-transparent">
          What kind of agent would you <br /> like to speak to today?
        </h2>
        <div className="content flex flex-col space-y-4 p-6 rounded-lg shadow-md bg-[#fca6ff]">
          {messages.map((message, index) => (
            <div key={index} className={`bg-[#b0ab5f] flex w-full ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}> 
              {message.type === 'user' ? (
                <GradientCard className="space-y-2">
                  <p>{message.content}</p>
                </GradientCard>
              ) : (
                <TextCard className="space-y-1">
                  <p>{message.content}</p>
                </TextCard>
              )}
            </div>
          ))}
          {fetching && (
            <div className="text-center">Loading response...</div>
          )}
          {error && (
            <div className="text-red-500">
              Error: {error.toString()}
            </div>
          )}
          <div ref={messagesEndRef} className="bg-[#66b05f]"/>
        </div>
      </div>

      <div
        className="fixed pt-3 px-60 pb-7 bottom-0 left-0 right-0 w-full bg-[#030711]">
        <div className="relative">
          <Input
            placeholder="Search for an agent..."
            className=" h-14 rounded-full bg-[#030711] border-gray-500 placeholder:text-gray-500 px-6 pr-14"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
              if (e.key === "Enter") {
                void handleSearch();
              }
            }}
          />
          {searchInput.trim() && (
            <Button 
              size="icon" 
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] hover:opacity-90"
              onClick={() => void handleSearch()}><Search className="h-4 w-4" /></Button>
          )}
        </div>
        </div>
    </div>
  );
}
