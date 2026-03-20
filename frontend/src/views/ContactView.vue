<template>
  <div>
    <section class="page-header">
      <h1>Contactez-nous</h1>
      <p>Nous serions ravis de vous entendre</p>
    </section>

    <section class="section">
      <div class="container">
        <div class="contact-grid">
          <div class="contact-info">
            <h2>Restons en contact</h2>
            <p>N'hésitez pas à nous écrire pour toute question, demande de partenariat ou information sur notre coopérative.</p>

            <div class="contact-details">
              <div class="contact-item">
                <div class="contact-icon"><i class="fas fa-map-marker-alt"></i></div>
                <div>
                  <h4>Adresse</h4>
                  <p>Obala, Village Nkolndobo, Cameroun</p>
                </div>
              </div>
              <div class="contact-item">
                <div class="contact-icon"><i class="fas fa-phone"></i></div>
                <div>
                  <h4>Téléphone</h4>
                  <p>+237 699 810 144 / +237 679 152 963</p>
                </div>
              </div>
              <div class="contact-item">
                <div class="contact-icon"><i class="fas fa-envelope"></i></div>
                <div>
                  <h4>Email</h4>
                  <p>contact@socopro.com</p>
                </div>
              </div>
              <div class="contact-item">
                <div class="contact-icon"><i class="fas fa-clock"></i></div>
                <div>
                  <h4>Horaires</h4>
                  <p>Lun - Ven : 8h00 - 17h00</p>
                </div>
              </div>
            </div>
          </div>

          <div class="contact-form-wrapper">
            <form @submit.prevent="submitForm" class="contact-form">
              <div class="form-group">
                <label for="nom">Nom complet *</label>
                <input id="nom" v-model="form.nom" type="text" required maxlength="100" placeholder="Votre nom" />
              </div>
              <div class="form-group">
                <label for="email">Email *</label>
                <input id="email" v-model="form.email" type="email" required maxlength="254" placeholder="votre@email.com" />
              </div>
              <div class="form-group">
                <label for="sujet">Sujet *</label>
                <input id="sujet" v-model="form.sujet" type="text" required maxlength="200" placeholder="Sujet de votre message" />
              </div>
              <div class="form-group">
                <label for="message">Message *</label>
                <textarea id="message" v-model="form.message" required maxlength="5000" placeholder="Votre message..." rows="6"></textarea>
              </div>

              <div class="form-alert success" v-if="success">
                <i class="fas fa-check-circle"></i>
                Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.
              </div>

              <div class="form-alert error" v-if="error">
                <i class="fas fa-exclamation-circle"></i>
                {{ error }}
              </div>

              <button type="submit" class="btn btn-primary" :disabled="submitting">
                <span v-if="submitting"><i class="fas fa-spinner fa-spin"></i> Envoi...</span>
                <span v-else><i class="fas fa-paper-plane"></i> Envoyer le message</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import api from '../api'

const form = reactive({
  nom: '',
  email: '',
  sujet: '',
  message: '',
})

const submitting = ref(false)
const success = ref(false)
const error = ref('')

async function submitForm() {
  submitting.value = true
  success.value = false
  error.value = ''

  try {
    await api.post('/contact/', { ...form })
    success.value = true
    form.nom = ''
    form.email = ''
    form.sujet = ''
    form.message = ''
  } catch (err) {
    error.value = "Une erreur est survenue. Veuillez réessayer plus tard."
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: start;
}

.contact-info h2 {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: var(--color-primary-dark);
  margin-bottom: 15px;
}

.contact-info > p {
  color: var(--color-text-light);
  margin-bottom: 30px;
  line-height: 1.8;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.contact-item {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.contact-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-icon i {
  color: var(--color-white);
  font-size: 1.1rem;
}

.contact-item h4 {
  font-size: 1rem;
  color: var(--color-primary-dark);
  margin-bottom: 3px;
}

.contact-item p {
  color: var(--color-text-light);
  font-size: 0.95rem;
}

.contact-form-wrapper {
  background: var(--color-white);
  padding: 40px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.contact-form button[type="submit"] {
  width: 100%;
}

.form-alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.form-alert i {
  margin-right: 8px;
}

.form-alert.success {
  background: #E8F5E9;
  color: #2E7D32;
  border: 1px solid #C8E6C9;
}

.form-alert.error {
  background: #FFEBEE;
  color: #C62828;
  border: 1px solid #FFCDD2;
}

@media (max-width: 768px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
  .contact-form-wrapper {
    padding: 25px;
  }
}
</style>
