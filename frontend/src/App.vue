<template>
  <main class="page">
    <section class="hero">
      <p class="eyebrow">Graduation Project</p>
      <h1>网络防沉迷预警系统</h1>
      <p class="summary">
        当前前端骨架已建立，后续将逐步接入行为画像、风险分析与预警解释页面。
      </p>
    </section>

    <section class="cards">
      <article class="card">
        <h2>今日概览</h2>
        <p>总使用时长、风险等级、高频 App 排行。</p>
      </article>
      <article class="card">
        <h2>行为画像</h2>
        <p>趋势、类别占比、夜间使用和高风险时间段分析。</p>
      </article>
      <article class="card">
        <h2>预警中心</h2>
        <p>历史预警、触发原因解释、用户反馈闭环。</p>
      </article>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 48px 24px;
  background:
    radial-gradient(circle at top left, rgba(39, 109, 255, 0.16), transparent 30%),
    linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%);
  color: #122033;
}

.hero {
  max-width: 760px;
  margin: 0 auto 32px;
}

.eyebrow {
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 12px;
  color: #4f7199;
}

h1 {
  margin: 0;
  font-size: clamp(36px, 6vw, 60px);
  line-height: 1.1;
}

.summary {
  margin-top: 16px;
  max-width: 600px;
  font-size: 18px;
  line-height: 1.7;
  color: #34506f;
}

.cards {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.card {
  padding: 24px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.75);
  box-shadow: 0 20px 40px rgba(38, 67, 104, 0.08);
  backdrop-filter: blur(10px);
}

.card h2 {
  margin-top: 0;
  margin-bottom: 12px;
}

.card p {
  margin: 0;
  line-height: 1.7;
  color: #4b6482;
}
</style>

