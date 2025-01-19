import { useFetch } from "@gadgetinc/react"; 
import { Search } from "lucide-react";
import { useState } from "react";
import { useOutletContext } from "@remix-run/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { RootOutletContext } from "../root";

export default function() {
  const { gadgetConfig } = useOutletContext<RootOutletContext>();
  const [searchInput, setSearchInput] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  
  const [{ data, error, fetching }, sendFetch] = useFetch(
    "https://collectionapi.metmuseum.org/public/collection/v1/objects/436535",
    { json: true, sendImmediately: false });
  
  const handleSearch = async () => {
    if (searchInput.trim()) {
      setHasSearched(true);
      await sendFetch();
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
          {!hasSearched && (
            <div className="text-center text-gray-500">
              
            </div>
          )}
          
          {hasSearched && (
           
            <>
              {fetching && (
              
                <div className="text-center">Loading artwork details...</div>
                  )}
              {data && !fetching && (
                <div className="space-y-4 bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] px-6 pt-6 pb-8 rounded-tl-[36px] rounded-tr-[6px] rounded-bl-[36px] rounded-br-[36px] text-black">
                  <h2 className="text-xl font-semibold">{data.title}</h2>
                  <p>{data.artistDisplayName}, {data.objectDate}</p>
                </div>
              
              )}

              {error && (
                <div className="text-red-500">Error loading artwork: {error.toString()}</div>
              )}
            </>
          )}
          
        </CardContent>
        <div className="relative w-full">
          <Input
            placeholder="Search for an agent..."
            className="mt-auto h-14 rounded-full border-[#7d7d7d] placeholder:text-gray-500 px-6 pr-14"
            disabled={fetching}
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
