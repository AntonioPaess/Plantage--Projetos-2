describe('Visualizar atividades diárias', () => {
    it('Deve visualizar as atividades diárias', () => {
        cy.visit('/')
        // Realizar login antes de cada teste
        const email = 'usuariotentativa@teste.com'
        cy.get('#id_login').type(email)
        cy.get('#id_password').type('A12345678.')
        cy.get('#id_remember').check()
        cy.get('button').click()
        
        //Adicionar Hortaliça ao canteiro
        cy.get('#atividades-icon').click() 
        

    })
})