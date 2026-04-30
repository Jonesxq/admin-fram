<script setup lang="ts">
import { getStatusLabel, getStatusTagType, type StatusValue } from '@/utils/status'

defineProps<{
  value: StatusValue
}>()
</script>

<template>
  <ElTag :type="getStatusTagType(value)" effect="light">
    {{ getStatusLabel(value) }}
  </ElTag>
</template>
