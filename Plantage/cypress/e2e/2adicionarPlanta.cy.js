
    

    describe('Adicionar e Visualizar Hortaliça', () => {
        it('deve adicionar uma alface e visualizar as informações dela', () => {
            cy.visit('/')
            // Realizar login antes de cada teste
            const email = 'usuariotentativa@teste.com'
            cy.get('#id_login').type(email)
            cy.get('#id_password').type('A12345678.')
            cy.get('#id_remember').check()
            cy.get('button').click()
            // Verificar se login foi bem sucedido
            
            // Navegar para página de adicionar planta
            cy.get('.navitems > :nth-child(2) > .flex').click()
            cy.get('#add').click()

            // Preencher formulário
            cy.get('#nome').type('Alface')
            cy.get('#ciclo_de_podagem').type('30')
            cy.get('#ciclo_de_colheita').type('60')

            // Upload da imagem
            cy.get('#imagem').selectFile('cypress/fixtures/imagens/alface.png')
            cy.get('[data-value="Alta"]').click()
            cy.get('#no_enemies').check()
            cy.get('.btn').click()


            // Visualizar planta
            cy.get('[href^="/plant/"]').first().click()

            
        })
    })
