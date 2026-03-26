import { flushPromises, mount } from "@vue/test-utils";

import HomePage from "@/pages/home/ui/HomePage.vue";

describe("HomePage", () => {
  it("renders the routed page and feature panel through shared UI primitives", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({
          status: "ok",
          service: "Fullstack Template API",
          checks: [
            {
              name: "postgresql",
              status: "ok",
              detail: "reachable",
            },
            {
              name: "redis",
              status: "error",
              detail: "connection timed out",
            },
          ],
        }),
      } satisfies Partial<Response>),
    );

    const wrapper = mount(HomePage);

    await flushPromises();
    await flushPromises();

    expect(wrapper.text()).toContain("This is the template baseline");
    expect(wrapper.text()).toContain("Reference system health slice");
    expect(wrapper.text()).toContain("Fullstack Template API");
    expect(wrapper.text()).toContain("postgresql");
    expect(wrapper.text()).toContain("redis");
  });
});
