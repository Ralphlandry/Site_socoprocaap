<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h3><img src="/LOGO (1).png" alt="SOCOPROCAAP" class="footer-logo" /> SOCOPROCAAP</h3>
          <p>Coopérative agropastorale spécialisée dans le cacao, le maïs, le gombo et l'élevage porcin. Nous cultivons l'excellence depuis des générations.</p>
        </div>
        <div class="footer-col">
          <h4>Navigation</h4>
          <ul>
            <li><router-link to="/">Accueil</router-link></li>
            <li><router-link to="/equipe">Équipe</router-link></li>
            <li><router-link to="/productions">Productions</router-link></li>
            <li><router-link to="/blog">Blog</router-link></li>
            <li><router-link to="/galerie">Galerie</router-link></li>
            <li><router-link to="/contact">Contact</router-link></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <ul>
            <li><i class="fas fa-map-marker-alt"></i> Obala, Village Nkolndobo, Cameroun</li>
            <li><i class="fas fa-phone"></i> +237 699 810 144</li>
            <li><i class="fas fa-phone"></i> +237 679 152 963</li>
            <li><i class="fas fa-envelope"></i> contact@socopro.com</li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Suivez-nous</h4>
          <div class="social-links">
            <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} SOCOPROCAAP. Tous droits réservés.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.footer {
  background: var(--color-primary-dark);
  color: var(--color-white);
  padding: 60px 0 20px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.footer-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  vertical-align: middle;
  margin-right: 5px;
}

.footer-col h3 {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-col h4 {
  font-size: 1.1rem;
  margin-bottom: 15px;
  color: var(--color-secondary);
}

.footer-col p {
  color: rgba(255,255,255,0.7);
  font-size: 0.95rem;
  line-height: 1.7;
}

.footer-col ul li {
  margin-bottom: 10px;
}

.footer-col ul li a,
.footer-col ul li {
  color: rgba(255,255,255,0.7);
  font-size: 0.95rem;
  transition: color 0.3s;
}

.footer-col ul li a:hover {
  color: var(--color-secondary);
}

.footer-col ul li i {
  margin-right: 8px;
  color: var(--color-secondary);
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  color: var(--color-white);
  transition: all 0.3s;
}

.social-links a:hover {
  background: var(--color-secondary);
  transform: translateY(-3px);
}

.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 20px;
  text-align: center;
  color: rgba(255,255,255,0.5);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
</style>
