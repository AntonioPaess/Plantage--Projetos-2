describe('Adicionar Hortaliça ao canteiro', () => {
    it('deve adicionar uma nova Hortaliça ao canteiro de plantação', () => {
        cy.visit('/')
        // Realizar login antes de cada teste
        const email = 'usuariotentativa@teste.com'
        cy.get('#id_login').type(email)
        cy.get('#id_password').type('A12345678.')
        cy.get('#id_remember').check()
        cy.get('button').click()
        
        //Adicionar Hortaliça ao canteiro
        cy.get('[id^="icon-"]').first().click() // Pega o primeiro ícone que começa com "icon-"
        cy.contains('Adicionar Planta').click() // Encontra pelo texto
        cy.get('[id^="planta-"]').first().click() // Pega a primeira planta
        cy.get('input[type="number"]').first().type('2') // Pega o primeiro input numérico
        cy.get('button').contains('Adicionar').click() // Encontra botão pelo texto
        cy.get('[id^="icon-"]').first().click() // Fecha o menu
    })
})