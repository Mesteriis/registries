import { mount } from "@vue/test-utils";

import App from "../../App.vue";


describe("App", () => {
  it("renders the base frontend shell", () => {
    const wrapper = mount(App);

    expect(wrapper.text()).toContain("Base Vue 3 application");
    expect(wrapper.text()).toContain("Vue 3 with script setup");
  });
});
