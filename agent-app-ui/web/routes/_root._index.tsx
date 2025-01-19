import { Search } from "lucide-react";
import { useFetch } from "@gadgetinc/react"; 
import { useState, useEffect } from "react";
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
  const [searchInput, setSearchInput] = useState("");
  const [submittedText, setSubmittedText] = useState("");

   const [{ data, error, fetching }, sendFetch] = useFetch(
    "https://collectionapi.metmuseum.org/public/collection/v1/objects/436535",
    { json: true, sendImmediately: false });

  // Trigger API call when `submittedText` changes
  useEffect(() => {
    if (submittedText) {
      void sendFetch();
    }
  }, [submittedText]);

  
  const handleSearch = async () => {
    if (searchInput.trim()) {
      setSubmittedText(searchInput.trim());
      setSearchInput("");
    }
  };

  return (
    <div className="relative flex w-full max-w-4xl">
      
      <Card className={cn(
        "flex-1 p-6 transition-all duration-300 border-none shadow-lg",
      )}>
        <CardHeader>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] bg-clip-text text-transparent">
            What kind of agent would you <br /> like to speak to today?
          </CardTitle>
        </CardHeader>
        
        <CardContent className="flex flex-col space-y-8 min-h-[300px] p-6 rounded-lg shadow-md">
        
           
          {submittedText && (
      <>
            <div className="flex justify-end w-full">
              <GradientCard className="space-y-2">
                <p>{submittedText}</p>
              </GradientCard>
            </div>


                    {/* Display Fetched Data */}
              {fetching && (
                <div className="text-center">Loading artwork details...</div>
              )}
              {data && !fetching && (
                <TextCard className="space-y-1">
                  <h2 className="text-xl font-semibold">{data.title}</h2>
                  <p>{data.artistDisplayName}, {data.objectDate}</p>
                </TextCard>
              )}
              {error && (
                <div className="text-red-500">
                  Error loading artwork: {error.toString()}
                </div>
              )}
        
      </>
          )}
        </CardContent>
        <div className="relative w-full">
          <Input
            placeholder="Search for an agent..."
            className="mt-auto h-14 rounded-full border-[#7d7d7d] placeholder:text-gray-500 px-6 pr-14"
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
      </Card>
    </div>
  );
}
