export type StatusValue = string | number | null | undefined

export function isEnabledStatus(value: StatusValue) {
  return value === 'enabled' || value === '1' || value === 1
}

export function getStatusLabel(value: StatusValue) {
  return isEnabledStatus(value) ? '启用' : '停用'
}

export function getStatusTagType(value: StatusValue) {
  return isEnabledStatus(value) ? 'success' : 'info'
}
