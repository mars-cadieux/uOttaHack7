import * as React from "react"
import { cn } from "@/lib/utils"

interface GradientCardProps {
  children: React.ReactNode
  className?: string
}

 
export const GradientCard: React.FC<GradientCardProps> = ({ children, className }) => {
  return (
    <div
      className={cn(
        "max-w-md rounded-lg bg-gradient-to-br from-[#ebcf73] to-[#9941e0] px-3 pt-2 pb-3 rounded-tl-[36px] rounded-tr-[6px] rounded-bl-[36px] rounded-br-[36px] text-black",
        className
      )}
    >{children}</div>
  )
}
