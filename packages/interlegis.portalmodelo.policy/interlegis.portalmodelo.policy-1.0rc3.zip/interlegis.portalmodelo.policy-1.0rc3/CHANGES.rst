Changelog
=========

1.0rc3 (2014-12-12)
-------------------

- Add portlet BuscaLeg as a default portlet
  [jeanferri]

- Change portlet name from 'Acesso à Informação' to 'Banners'
  [jeanferri]


1.0rc2 (2014-10-24)
-------------------

- Register some dependencies
  [jeanferri]

- Change social media icons
  [jeanferri]

- Change 'Redes Sociais' portlet name to 'Mídias Sociais'
  [jeanferri]

- Added a link content referencing to Portal Modelo 3 user manual
  [jeanferri]

- Removed collective.weather from default installation of Portal Modelo
  [jeanferri]

- Disabled discussion moderation because Intranet conflict
  [jeanferri]

- Added 2 collections to folders 'Galeria de Áudios' and 'Galeria de Fotos'
  [jeanferri]

- Imported some photos inside 'Banco de Imagens' as an example gallery
  [jeanferri]

- Moved all importing images to browser/images directory
  [jeanferri]

- Added Youtube video embedder in /institucional/videos as an example
  [jeanferri]

- Added default video as a link to a MP4 file and videos default view
  [jeanferri]

- Added a link to MP3 example file in /institucional/audio
  [jeanferri]

- Enabled Rádio Legislativa portlet
  [jeanferri]

- Enable name display for Anonymous users on Foruns (PloneBoard)
  [ericof]

- Added Rádio Legislativa structure including a folder for audios and a portlet
  [jeanferri]

- Fix Discussion Item workflow and settings
  [ericof]

- Add coveralls.io support
  [ericof]

- Fix Travis configuration for this package
  [ericof]

- Added collective.flowplayer to provide a player for MP3 and MP4 local files
  [jeanferri]

- Removed front-page and footer-page objects from sitemap
  [jeanferri]


1.0rc1 (2014-08-30)
-------------------

- Changed home page id from 'pagina-inicial' to 'front-page' for internationalization
  [jeanferri]

- Added 'Nossos Parlamentares' Cover tile in the portal home
  [jeanferri]

- Added Clipping folder in 'Sobre a Câmara' section
  [jeanferri]

- Changed newsletter id from /boletins/acompanhe-a-camara to /boletins/aconpanhe
  for generalization
  [jeanferri]

- Added portlet "Acesso à Informação" as a banner in static portlet
  [jeanferri]

- Changed folder id from sobre-a-camara to institucional for generalization
  [jeanferri]

- Added TV Legislativa structure including a folder for videos and a portlet
  [jeanferri]


1.0b4 (2014-08-25)
------------------

- Refactoring content creation on sobre-a-camara structure and it contents
  [jeanferri]

- Changed /imagens and /sobre-a-camara/fotos default_view
  [jeanferri]

- Change collection default_view to summary_view
  [jeanferri]

- Adding youtube and pinterest icons to 'Redes Sociais' portlet
  [jeanferri]

- Adding RSS page to main navigation
  [jeanferri]

- Adding 'Acesso à Informação' page content and image
  [jeanferri]

- Reorder right portlets and tests fixing for default content creation
  [jeanferri]

- Override default view for Zope Root
  [ericof]

- Override new site creation form
  [ericof]

- Changing 'Home' link to portal_url to avoid Intranet owning home link
  [jeanferri]

- Enable syndication by default
  [ericof]

- Changed default footer navigation
  [jeanferri]

- Changed Folder default_view to folder_summary_view
  [ericof]

- Enable live search and fix searchable content types (https://colab.interlegis.leg.br/ticket/2962).
  [hvelarde]

- Fix content types displayed on navigation (https://colab.interlegis.leg.br/ticket/2961).
  [hvelarde]

- Add ods, odt, odp, html, csv, zip, tgz, ppt, pptx, xls and xlsx to the list
  of file types that can be uploaded to the portal (https://colab.interlegis.leg.br/ticket/2966).
  [hvelarde]

- Refactored folders structure from the root folder of portal.
  [jeanferri]

- Os ícones dos tipos de conteúdo só devem se mostrar para usuários autenticados (https://colab.interlegis.leg.br/ticket/2972).
  [hvelarde]


1.0b3 (2014-07-02)
------------------

- Cria boletim padrão e adiciona portlet de assinatura (https://colab.interlegis.leg.br/ticket/2879).
  [hvelarde]


1.0b2 (2014-06-05)
------------------

- O ``comment_review_workflow`` é agora o workflow padrão para comentários;
  Moderação habilitada.

- Adiciona como dependência o ``interlegis.portalmodelo.transparency``.

- Remove ``portal_tabs`` e habilita as seções por pasta.

- Adiciona como dependência o ``plone.app.event``; instala e configura a
  versão Archetypes.


1.0b1 (2014-05-16)
------------------

- Modifica texto do rodape (`#2918`_).

- O portlet de Sessões on-line fica oculto por padrão.

- Foram corrigidos os links aos ícones no portlet de Redes sociais.


1.0a11 (2014-05-01)
-------------------

- Enquete sobre o Portal foi habilitada (`#2878`_).

- Ajustes na configuração dos comentários no site (`#2880`_).

- Adiciona o ``/blog`` na estrutura do site (`#2876`_).


1.0a10 (2014-04-27)
-------------------

- Correções na i18n do pacote.

- Webservice de entrega de dados (em formato aberto) da casa legislativa, de
  parlamentares, etc. (`#2885`_).

- Sistema de informações ao cidadão (`#2884`_).

- Novo sistema de transparência (prestação de contas) com suporte a dados
  abertos (`#2883`_).


1.0a9 (2014-04-08)
------------------

- Painel de parlamentares, legislatura e mesa diretora, que funcione local ou
  integrado ao SAPL (`#2857`_).

- Melhorar a integração com sistemas do processo legislativo (`#2855`_).

- Integração com o LexML (`#2856`_).

- Revisar e reestruturar toda a árvore de informação padrão do Portal Modelo
  (`#2853`_).

- Adiciona o pacote `brasil.gov.vcge`_.


1.0a8 (2014-03-12)
------------------

- Adiciona (mas não instala) ``interlegis.intranetmodelo`` como uma
  depêndencia do projeto (`#2872`_).


1.0a7 (2013-11-29)
------------------

- Implementa nova Arquitetura da Informação.


1.0a6 (2013-11-29)
------------------

- Remove inclusão de skin.


1.0a5 (2013-11-11)
------------------

- Ferramentas multimídia (`#2744`_, `#2745`_ e `#2746`_).


1.0a4 (2013-11-08)
------------------

- Ferramentas de redes sociais integradas no portal.


1.0a3 (2013-11-08)
------------------

- Nova ferramenta de publicação da página inicial com melhor usabilidade
  (`#2736`_).


1.0a2 (2013-11-01)
------------------

- Inclusão da ferramenta de boletins eletrônicos (newsletter) (`#2692`_).

- Inclusão da ferramenta de blog para parlamentares e funcionários da casa
  (`#2689`_).

- Comentários habilitados com controle de captcha, moderação e aviso por
  e-mail (`#2735`_).

- Inclusão da ferramenta de previsão do tempo (`#2693`_).

- Visão de agenda habilitada.

- Inclusão da ferramenta de enquetes (`#2691`_).

- Inclusão da ferramenta de formulários.

- Inclusão de upload de múltiplos arquivos e imagens (`#2733`_).

- Inclusão da ferramenta de fórum (`#2690`_).


1.0a1 (2013-10-28)
------------------

- Release inicial.

.. _`#2689`: http://colab.interlegis.leg.br/ticket/2689
.. _`#2690`: http://colab.interlegis.leg.br/ticket/2690
.. _`#2691`: http://colab.interlegis.leg.br/ticket/2691
.. _`#2692`: http://colab.interlegis.leg.br/ticket/2692
.. _`#2693`: http://colab.interlegis.leg.br/ticket/2693
.. _`#2733`: http://colab.interlegis.leg.br/ticket/2733
.. _`#2735`: http://colab.interlegis.leg.br/ticket/2735
.. _`#2736`: http://colab.interlegis.leg.br/ticket/2736
.. _`#2744`: http://colab.interlegis.leg.br/ticket/2744
.. _`#2745`: http://colab.interlegis.leg.br/ticket/2745
.. _`#2746`: http://colab.interlegis.leg.br/ticket/2746
.. _`#2853`: https://colab.interlegis.leg.br/ticket/2853
.. _`#2855`: https://colab.interlegis.leg.br/ticket/2855
.. _`#2856`: https://colab.interlegis.leg.br/ticket/2856
.. _`#2857`: https://colab.interlegis.leg.br/ticket/2857
.. _`#2872`: https://colab.interlegis.leg.br/ticket/2872
.. _`#2876`: https://colab.interlegis.leg.br/ticket/2876
.. _`#2878`: https://colab.interlegis.leg.br/ticket/2878
.. _`#2880`: https://colab.interlegis.leg.br/ticket/2880
.. _`#2883`: https://colab.interlegis.leg.br/ticket/2883
.. _`#2884`: https://colab.interlegis.leg.br/ticket/2884
.. _`#2885`: https://colab.interlegis.leg.br/ticket/2885
.. _`#2918`: https://colab.interlegis.leg.br/ticket/2918
.. _`brasil.gov.vcge`: https://pypi.python.org/pypi/brasil.gov.vcge
