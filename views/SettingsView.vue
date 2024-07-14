<template>
  <div id="settings">
    <header>
			<nav>
				<div class="header">
				<img class="logo" src="@/assets/logo.png" alt="Logo Pong Ft_Transcendence">
				<h1 class="title">SETTINGS</h1>
				</div>
			</nav>
		</header>
    <main>
      <section class="settings-buttons">
        <table>
          <tr>
            <td></td>
            <td>
              <router-link to="/settings/settings_general" class="glowing-btn">
                <span class="glowing-txt">GE<span class="faulty-letter">NER</span>AL</span>
              </router-link>
            </td>
            <td></td>
          </tr>
          <tr>
            <td>
              <router-link to="/settings/graphics" class="glowing-btn">
                <span class="glowing-txt"><span class="faulty-letter">GRA</span>P<span class="faulty-letter">HI</span>CS</span>
              </router-link>
            </td>
            <td></td>
            <td>
              <router-link to="/settings/credits" class="glowing-btn">
                <span class="glowing-txt">CRE<span class="faulty-letter">DIT</span>S</span>
              </router-link>
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <router-link to="/settings/settings_audio" class="glowing-btn">
                <span class="glowing-txt">A<span class="faulty-letter">U</span>D<span class="faulty-letter">I</span>O</span>
              </router-link>
            </td>
            <td></td>
          </tr>
        </table>
      </section>
    </main>
    <footer>
        <div class="footer">
          <img class="logo" src="@/assets/logo.png" alt="Logo Pong Ft_Transcendence">
        </div>
    </footer>
  </div>
</template>

<script setup>

</script>

<style scoped>

@import '../styles/MainStyle.css';

</style>
