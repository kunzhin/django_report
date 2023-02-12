$(function () {
    $('div[class^="box-sort-menu-"]').click(function (){

        const idValue = $(this).attr('id')

        let nodeList = $("div.info-tt")

        let itemsArray = []
        let itemsIntArray = []
        let itemsStrArray = []
        let parent = nodeList[0].parentNode
        for (let i = 0; i < nodeList.length; i++) {
            itemsArray.push(parent.removeChild(nodeList[i]));
        }

        itemsArray.forEach((item) => {
            const value = item.querySelector(
                "div[class~="+ idValue +"]"
            ).querySelector("span").textContent

            if (value.length === 0 || !isFinite(value.trim())) {
                itemsStrArray.push(item)
            } else {
                itemsIntArray.push(item)
            }

        })

        itemsStrArray.sort((a, b) => {
            let textA = a.querySelector(
                "div[class~="+ idValue +"]"
            ).querySelector("span").textContent

            let textB = b.querySelector(
                "div[class~="+ idValue +"]"
            ).querySelector("span").textContent

            if (textA.length === 0) return 1
            if (textB.length === 0) return -1
            if (textA < textB) return -1
            if (textA > textB) return 1
            return 0
        })

        itemsIntArray.sort((a, b) => {
            let textA = a.querySelector(
                "div[class~="+ idValue +"]"
            ).querySelector("span").textContent

            let textB = b.querySelector(
                "div[class~="+ idValue +"]"
            ).querySelector("span").textContent

            if (parseInt(textA) < parseInt(textB)) return -1
            if (parseInt(textA) > parseInt(textB)) return 1
            return 0
        })

        itemsIntArray.push(...itemsStrArray)

        itemsIntArray.forEach((node) => {
            parent.appendChild(node)
        })
    })
})