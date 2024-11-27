    describe('Adicionar Espaço e Canteiro', () => {
        it('deve adicionar um espaço e um canteiro dentro desse espaço', () => {
            cy.visit('/')
            // Realizar login antes de cada teste
            const email = 'usuariotentativa@teste.com'
            cy.get('#id_login').type(email)
            cy.get('#id_password').type('A12345678.')
            cy.get('#id_remember').check()
            cy.get('button').click()
            // Verificar se login foi bem sucedido
            
            // Adicionar Espaço
            cy.get('.aspect-square').click()
            cy.get('#nome').type('Horta do João')
            cy.get('#quantMaxCanteiro').type('10')

            cy.get('#tipo_de_solo').select('Solo Argiloso')
            // Envia formulário
            cy.get('.bg-green-400').click()

            //Adicionar canteiro
            cy.get(':nth-child(1) > .py-4 > .shadow-sm').click()
            cy.get('#nome').type('Vegetais')
            cy.get('#quantMaxPlant').type('5')
            cy.get('.bg-green-400').click()
            cy.get('.block > .justify-between').click()
        })
    })