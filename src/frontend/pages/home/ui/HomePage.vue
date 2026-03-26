<script setup lang="ts">
import { onMounted } from "vue";

import { SystemHealthPanel } from "@/features/system-health";
import { trackPageMountComplete } from "@/shared/observability";
import {
  AppCard,
  AppSection,
  AppStack,
  AppText,
} from "@/shared/ui";

onMounted(() => {
  trackPageMountComplete("home", {
    route: "home",
  });
});
</script>

<template>
  <AppStack gap="lg">
    <AppSection
      title="This is the template baseline"
      description="The homepage explains the reusable engineering baseline. It is intentionally not a product dashboard."
    >
      <AppStack gap="md">
        <AppCard
          title="What is already implemented"
          description="The template already includes layered frontend structure, typed API access, observability wiring, strict checks and ADR-driven governance."
        >
          <AppText
            as="p"
            tone="muted"
          >
            Pages stay thin, features own reusable flows, and shared/ui remains the only primitive surface. Local App* primitives are intentionally shaped for low-cost migration to an external UI kit.
          </AppText>
        </AppCard>

        <SystemHealthPanel />
      </AppStack>
    </AppSection>
  </AppStack>
</template>
