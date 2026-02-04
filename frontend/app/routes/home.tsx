import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Expense Flow" },
    { name: "description", content: "Expense Flow is a personal budgeting app" },
  ];
}

export default function Home() {
  return <Welcome />;
}
