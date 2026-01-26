"use client";

import { EyeClosedIcon, EyeIcon, LockIcon } from "lucide-react";
import { useState } from "react";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";

export function PasswordInput({
  type,
  ...props
}: React.ComponentProps<typeof InputGroupInput>) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <InputGroup>
      <InputGroupInput
        placeholder="Password"
        type={showPassword ? "text" : "password"}
        {...props}
      />
      <InputGroupAddon>
        <LockIcon />
      </InputGroupAddon>
      <InputGroupAddon align="inline-end">
        {showPassword ? (
          <EyeIcon
            className="cursor-pointer"
            onClick={() => setShowPassword(!showPassword)}
          />
        ) : (
          <EyeClosedIcon
            className="cursor-pointer"
            onClick={() => setShowPassword(!showPassword)}
          />
        )}
      </InputGroupAddon>
    </InputGroup>
  );
}
