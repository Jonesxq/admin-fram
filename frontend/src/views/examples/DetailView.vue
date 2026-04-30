<script setup lang="ts">
const basicInfo = [
  ['单据编号', 'REQ-20260430-018'],
  ['申请人', '张三'],
  ['所属部门', '产品研发部'],
  ['当前状态', '审批中'],
  ['创建时间', '2026-04-30 09:18'],
  ['更新时间', '2026-04-30 16:42']
]

const auditInfo = [
  ['直属主管', '已通过'],
  ['财务复核', '处理中'],
  ['归档节点', '待处理']
]

const timeline = [
  { title: '提交申请', content: '张三提交采购申请', time: '2026-04-30 09:18' },
  { title: '主管审批', content: '李四审批通过', time: '2026-04-30 11:05' },
  { title: '财务复核', content: '等待财务确认预算科目', time: '2026-04-30 16:42' }
]
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">详情示例</h1>
        <p class="oa-page__desc">展示只读详情、分组字段和流程时间线。</p>
      </div>
      <ElTag type="warning" size="large">审批中</ElTag>
    </header>

    <section class="oa-stat-grid">
      <div class="oa-stat">
        <p class="oa-stat__label">申请金额</p>
        <p class="oa-stat__value">￥28,600</p>
      </div>
      <div class="oa-stat">
        <p class="oa-stat__label">审批节点</p>
        <p class="oa-stat__value">2 / 3</p>
      </div>
      <div class="oa-stat">
        <p class="oa-stat__label">预计完成</p>
        <p class="oa-stat__value">2 天</p>
      </div>
    </section>

    <section class="detail-grid">
      <div>
        <h2 class="detail-title">基础信息</h2>
        <ElDescriptions :column="2" border>
          <ElDescriptionsItem v-for="[label, value] in basicInfo" :key="label" :label="label">
            {{ value }}
          </ElDescriptionsItem>
        </ElDescriptions>
      </div>

      <div>
        <h2 class="detail-title">审批状态</h2>
        <ElDescriptions :column="1" border>
          <ElDescriptionsItem v-for="[label, value] in auditInfo" :key="label" :label="label">
            <ElTag :type="value === '已通过' ? 'success' : value === '处理中' ? 'warning' : 'info'">
              {{ value }}
            </ElTag>
          </ElDescriptionsItem>
        </ElDescriptions>
      </div>
    </section>

    <section class="oa-section">
      <h2 class="detail-title">流程记录</h2>
      <ElTimeline>
        <ElTimelineItem
          v-for="item in timeline"
          :key="item.time"
          :timestamp="item.time"
          placement="top"
        >
          <strong>{{ item.title }}</strong>
          <p class="detail-timeline__content">{{ item.content }}</p>
        </ElTimelineItem>
      </ElTimeline>
    </section>
  </div>
</template>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
  gap: 18px;
  margin-bottom: 18px;
}

.detail-title {
  margin: 0 0 12px;
  font-size: 15px;
  font-weight: 800;
}

.detail-timeline__content {
  margin: 8px 0 0;
  color: var(--oa-muted);
}

@media (max-width: 900px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
