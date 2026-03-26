import {
  createRouter,
  createWebHistory,
  type Router,
  type RouteRecordRaw,
  type RouterHistory,
} from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: () => import("@/pages/home/ui/HomePage.vue"),
    meta: {
      title: "Fullstack template frontend",
      description: "Layered shell, shared UI boundary, typed API access and a reference system slice.",
      lazy: true,
    },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/pages/not-found/ui/NotFoundPage.vue"),
    meta: {
      title: "Route not found",
      description: "The router resolves unknown paths through an explicit not-found route.",
      lazy: true,
    },
  },
];

export function createAppRouter(
  history: RouterHistory = createWebHistory(import.meta.env.BASE_URL),
): Router {
  return createRouter({
    history,
    routes,
    scrollBehavior() {
      return { top: 0 };
    },
  });
}
