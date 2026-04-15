<template>
  <a
    href="https://wa.me/237699810144?text=Bonjour,%20j'aimerais%20des%20informations"
    target="_blank"
    rel="noopener noreferrer"
    class="whatsapp-button"
    aria-label="Contactez-nous sur WhatsApp"
    title="Contactez-nous sur WhatsApp"
  >
    <i class="fab fa-whatsapp"></i>
  </a>
</template>

<style scoped>
.whatsapp-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #25D366 0%, #20BA5E 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
  transition: all 0.3s ease;
  z-index: 99;
  text-decoration: none;
}

.whatsapp-button:hover {
  transform: scale(1.1) translateY(-5px);
  box-shadow: 0 8px 30px rgba(37, 211, 102, 0.6);
}

.whatsapp-button:active {
  transform: scale(0.95);
}

/* Pulse animation au chargement */
@keyframes pulse {
  0% {
    box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
  }
  50% {
    box-shadow: 0 4px 30px rgba(37, 211, 102, 0.8);
  }
  100% {
    box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
  }
}

.whatsapp-button {
  animation: pulse 2s infinite;
}

@media (max-width: 768px) {
  .whatsapp-button {
    bottom: 20px;
    right: 20px;
    width: 55px;
    height: 55px;
    font-size: 26px;
  }
}

@media (max-width: 480px) {
  .whatsapp-button {
    bottom: 15px;
    right: 15px;
    width: 50px;
    height: 50px;
    font-size: 24px;
  }
}
</style>
