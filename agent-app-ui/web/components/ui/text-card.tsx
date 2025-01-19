import { type ComponentProps, type FC } from "react"
import { cn } from "@/lib/utils"

export function TextCard({ 
  children, 
  className,
  ...props
}: ComponentProps<"div">) {
  return (
    <div
      className={cn(
        "text-left max-w-md px-3 pt-2 pb-3 rounded-[36px] rounded-tr-[6px]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}