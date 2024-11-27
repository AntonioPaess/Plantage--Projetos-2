  
    // Testes de Autenticação
    describe('Autenticação', () => {
      beforeEach(() => {
        // Visita a página inicial antes de cada teste
        cy.visit('/')
      })
      // Teste de Cadastro
      it('deve fazer cadastro com sucesso', () => {
        const email = `usuariotentativa@teste.com`

        cy.get('.navitems > :nth-child(2) > a').click()
        cy.get('#id_email').type(email)
        cy.get('#id_username').type('Tentativa')
        cy.get('#id_password1').type('A12345678.')
        cy.get('#id_password2').type('A12345678.')
        cy.get('button').click()
        cy.get('.button').click()
      })
    }) // Fechamento do describe Autenticação    
