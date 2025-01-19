import { useFetch } from "@gadgetinc/react"; 
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
    }
  };

  return (
    <div className="relative flex w-full max-w-4xl">
      
      <Card className={cn(
        "flex-1 p-8 transition-all duration-300",
      )}>
        <CardHeader>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] bg-clip-text text-transparent">
            What kind of agent would you <br /> like to speak to today?
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col space-y-16 min-h-[300px]">
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
                <div className="space-y-4">
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
        <Input
            placeholder="Search for an agent..."
            className="mt-auto text-lg h-14 rounded-full border-[#7d7d7d] placeholder:text-gray-500"
            disabled={fetching}
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
              if (e.key === "Enter") {
                void handleSearch();
              }
            }}
          />
      </Card>
    </div>
  );
}
