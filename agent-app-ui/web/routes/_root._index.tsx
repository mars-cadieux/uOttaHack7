import { useState } from "react";
import { useFetch } from "@gadgetinc/react";
import { useOutletContext, Link } from "@remix-run/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { RootOutletContext } from "../root";

export default function() {
  const { gadgetConfig } = useOutletContext<RootOutletContext>();
  const [isAsideOpen, setIsAsideOpen] = useState(false);
  const [{ data: catFacts, error, fetching }, fetchCatFacts] = useFetch("/cat-facts", { json: true, sendImmediately: false });
  const [hasSearched, setHasSearched] = useState(false);

  return (
    <div className="relative flex w-full max-w-4xl">
      
      <Card className={cn(
        "flex-1 p-8 transition-all duration-300",
      )}>
        <CardHeader>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-[#f7dd88] to-[#ac45ff] bg-clip-text text-transparent">
            What kind of agent would you <br/> like to speak to today?
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col space-y-16 min-h-[300px]">
          <Input
            placeholder="Search for an agent..."
            className="mt-auto text-lg h-14 rounded-full border-[#7d7d7d] placeholder:text-gray-500"
            disabled={fetching}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                console.log("TESTTTTT")
              }
            }}
          />
        </CardContent>
      </Card>
    </div>
  );
}
