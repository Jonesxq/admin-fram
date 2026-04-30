<script setup lang="ts">
import { computed } from 'vue'

import { useAuthStore } from '@/stores/auth'

defineOptions({
  inheritAttrs: false
})

const props = withDefaults(
  defineProps<{
    permission: string | string[]
    mode?: 'all' | 'any'
    type?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'default'
    size?: 'large' | 'default' | 'small'
    disabled?: boolean
    loading?: boolean
    plain?: boolean
    text?: boolean
    link?: boolean
    round?: boolean
    circle?: boolean
  }>(),
  {
    mode: 'any',
    type: 'primary',
    size: 'default',
    disabled: false,
    loading: false,
    plain: false,
    text: false,
    link: false,
    round: false,
    circle: false
  }
)

const authStore = useAuthStore()

const allowed = computed(() => {
  const permissions = Array.isArray(props.permission) ? props.permission : [props.permission]

  if (props.mode === 'all') {
    return permissions.every(permission => authStore.hasPermission(permission))
  }

  return permissions.some(permission => authStore.hasPermission(permission))
})
</script>

<template>
  <ElButton
    v-if="allowed"
    v-bind="$attrs"
    :circle="circle"
    :disabled="disabled"
    :link="link"
    :loading="loading"
    :plain="plain"
    :round="round"
    :size="size"
    :text="text"
    :type="type"
  >
    <slot />
  </ElButton>
</template>
