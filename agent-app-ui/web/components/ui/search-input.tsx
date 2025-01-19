import * as React from "react"
import { SearchIcon } from "lucide-react"
import { Button } from "./button"
import { Input } from "./input"
import { cn } from "@/lib/utils"

export interface SearchInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onSearch: (value: string) => void
  placeholder?: string
}

const SearchInput = React.forwardRef<HTMLInputElement, SearchInputProps>(
  ({ className, onSearch, placeholder = "Search...", ...props }, ref) => {
    const [value, setValue] = React.useState("")

    const handleSearch = React.useCallback(() => {
      if (value.trim()) {
        onSearch(value.trim())
      }
    }, [value, onSearch])

    const handleSubmit = React.useCallback(
      (event: React.FormEvent) => {
        event.preventDefault()
        handleSearch()
      },
      [handleSearch]
    )

    return (
      <form onSubmit={handleSubmit} className={cn("flex w-full gap-2", className)}>
        <Input
          ref={ref}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={placeholder}
          className="flex-1"
          {...props}
        />
        <Button
          onClick={handleSearch}
          type="submit"
          className="bg-gradient-to-r from-purple-600 to-blue-500 text-white hover:from-purple-700 hover:to-blue-600"
        >
          <SearchIcon className="h-4 w-4" />
          <span className="ml-2">Search</span>
        </Button>
      </form>
    )
  }
)
SearchInput.displayName = "SearchInput"

export default SearchInput