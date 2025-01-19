import { json, LoaderFunctionArgs, redirect } from "@remix-run/node";
import { Outlet, useOutletContext } from "@remix-run/react";

export const loader = async ({ context }: LoaderFunctionArgs) => {
  const { session } = context;

  // redirect already logged in users to the app experience
  if (!!session?.get("user")) {
    return redirect("/signed-in");
  }

  return json({});
};

export default function () {
  const context = useOutletContext();

  return (
 
    <div className="w-full flex flex-col relative">
      <Outlet context={context} />
    </div>
  );
}
