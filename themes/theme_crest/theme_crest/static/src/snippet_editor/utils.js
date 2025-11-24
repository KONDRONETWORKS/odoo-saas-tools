/** @odoo-module **/

export const ORDER_BY = [
  { orderBy: "list_price asc", title: "Price: Low to High" },
  { orderBy: "list_price desc", title: "Price: High to Low" },
  { orderBy: "name asc", title: "Name: A to Z" },
  { orderBy: "name desc", title: "Name: Z to A" },
  { orderBy: "create_date desc", title: "Newly Arrived" },
  { orderBy: "bits_sales_count desc", title: "Best seller" },
  { orderBy: "rating_avg desc", title: "High rated" },
];

export const DEFAULT_TEMPLATE = [
  // { id: "default", title: "Default" }, // to-do
  { id: "new-arrival", title: "New arrival", orderBy: "create_date desc", tmp_for: 'product' },
  { id: "best-seller", title: "Best seller", orderBy: "bits_sales_count desc", tmp_for: 'product' },
  { id: "discounted-product", title: "Discounted product", tmp_for: 'product' },
  // { id: "top-rated", title: "Top rated", orderBy: "rating_avg desc", tmp_for: 'product' },
  { id: "a_to_z", title: "A to Z", orderBy: "name asc", tmp_for: 'category' },
  { id: "z_to_a", title: "Z to A", orderBy: "name desc", tmp_for: 'category' },
  { id: "a_to_z", title: "A to Z", orderBy: "name asc", tmp_for: 'blog' },
  { id: "z_to_a", title: "Z to A", orderBy: "name desc", tmp_for: 'blog' },
];
export const CATEGORIES = [
  { categoryTitle: 'Banner', categoryId: "banner" },
  { categoryTitle: 'Banner Slider', categoryId: "bannerslider" },
  { categoryTitle: 'Image Blocks', categoryId: "imageblocks" },
  { categoryTitle: 'Video Blocks', categoryId: "videoblocks" },
  { categoryTitle: 'Titles', categoryId: "titles" },
  { categoryTitle: 'About', categoryId: "about" },
  { categoryTitle: 'Call To Action', categoryId: "call_to_action" },
  { categoryTitle: 'Clients', categoryId: "clients" },
  { categoryTitle: 'Contact', categoryId: "contact" },
  { categoryTitle: 'Facts', categoryId: "facts" },
  { categoryTitle: 'FAQ', categoryId: "faq" },
  { categoryTitle: 'Features', categoryId: "features" },
  { categoryTitle: 'Hero', categoryId: "hero" },
  { categoryTitle: 'Portfolio', categoryId: "portfolio" },
  // { categoryTitle: 'Pricing', categoryId: "pricing" },
  { categoryTitle: 'Process', categoryId: "process" },
  { categoryTitle: 'Team', categoryId: "team" },
  { categoryTitle: 'Testimonials', categoryId: "testimonials" },
]

export const TEMPATE = [
  { id: "dy_prod_tmp_style_1_bits", title: "Product Style 1", tmp_for: 'product' },
  { id: "dy_prod_tmp_style_2_bits", title: "Product Style 2", tmp_for: 'product' },
  { id: "dy_prod_tmp_style_3_bits", title: "Product Style 3", tmp_for: 'product' },
  { id: "dy_prod_tmp_style_4_bits", title: "Product Style 4", tmp_for: 'product' },
  { id: "dy_prod_tmp_style_5_bits", title: "Product Style 5", tmp_for: 'product' },
  { id: "dy_categ_tmp_style_1_bits", title: "Category Style 1", tmp_for: 'category' },
  { id: "dy_categ_tmp_style_2_bits", title: "Category Style 2", tmp_for: 'category' },
  { id: "dy_categ_tmp_style_3_bits", title: "Category Style 3", tmp_for: 'category' },
  { id: "dy_categ_tmp_style_4_bits", title: "Category Style 4", tmp_for: 'category' },
  { id: "dy_blog_tmp_style_1_bits", title: "Blog Style 1", tmp_for: 'blog' },
  { id: "dy_blog_tmp_style_2_bits", title: "Blog Style 2", tmp_for: 'blog' },
  // { id: "dy_blog_tmp_style_3_bits", title: "Blog Style 3", tmp_for: 'blog' },

  // Banner
  { id: "theme_crest.s_banner_1_bits", title: "Banner 1", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-1.svg' },
  { id: "theme_crest.s_banner_2_bits", title: "Banner 2", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-5.svg' },
  { id: "theme_crest.s_banner_3_bits", title: "Banner 3", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-4.svg' },
  { id: "theme_crest.s_banner_4_bits", title: "Banner 4", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-3.svg' },
  { id: "theme_crest.s_banner_5_bits", title: "Banner 5", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-2.svg' },
  { id: "theme_crest.s_banner_6_bits", title: "Banner 6", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-6.svg' },
  { id: "theme_crest.s_banner_7_bits", title: "Banner 7", type: "static_template", category: "banner", image: '/theme_crest/static/images/web-images/banner/banner-1.svg' },

  // Image Blocks
  { id: "theme_crest.s_image_blocks_1_bits", title: "Image Blocks 1", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-6.svg' },
  { id: "theme_crest.s_image_blocks_2_bits", title: "Image Blocks 2", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-5.svg' },
  { id: "theme_crest.s_image_blocks_3_bits", title: "Image Blocks 3", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-2.svg' },
  { id: "theme_crest.s_image_blocks_4_bits", title: "Image Blocks 4", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-4.svg' },
  { id: "theme_crest.s_image_blocks_5_bits", title: "Image Blocks 5", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-3.svg' },
  { id: "theme_crest.s_image_blocks_6_bits", title: "Image Blocks 6", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-1.svg' },
  { id: "theme_crest.s_image_blocks_7_bits", title: "Image Blocks 7", type: "static_template", category: "imageblocks", image: '/theme_crest/static/images/web-images/img-blocks/img-blocks-7.svg' },


  // Banner Slider
  { id: "theme_crest.s_banner_slider_1_bits", title: "Banner Slider 1", type: "static_template", category: "bannerslider", image: '/theme_crest/static/images/web-images/bannerslider/slide-2.svg' },
  { id: "theme_crest.s_banner_slider_2_bits", title: "Banner Slider 2", type: "static_template", category: "bannerslider", image: '/theme_crest/static/images/web-images/bannerslider/slide-3.svg' },
  { id: "theme_crest.s_banner_slider_3_bits", title: "Banner Slider 3", type: "static_template", category: "bannerslider", image: '/theme_crest/static/images/web-images/bannerslider/slide-4.svg' },
  { id: "theme_crest.s_banner_slider_4_bits", title: "Banner Slider 4", type: "static_template", category: "bannerslider", image: '/theme_crest/static/images/web-images/bannerslider/slide-1.svg' },
  { id: "theme_crest.s_banner_slider_5_bits", title: "Banner Slider 5", type: "static_template", category: "bannerslider", image: '/theme_crest/static/images/web-images/bannerslider/slide-5.svg' },

  // Video Blocks
  { id: "theme_crest.s_video_1_bits", title: "Video Blocks 1", type: "static_template", category: "videoblocks", image: '/theme_crest/static/images/web-images/videobanner/video-blocks-1.svg' },
  { id: "theme_crest.s_video_2_bits", title: "Video Blocks 2", type: "static_template", category: "videoblocks", image: '/theme_crest/static/images/web-images/videobanner/video-blocks-2.svg' },
  { id: "theme_crest.s_video_3_bits", title: "Video Blocks 3", type: "static_template", category: "videoblocks", image: '/theme_crest/static/images/web-images/videobanner/video-blocks-5.svg' },
  { id: "theme_crest.s_video_4_bits", title: "Video Blocks 4", type: "static_template", category: "videoblocks", image: '/theme_crest/static/images/web-images/videobanner/video-blocks-3.svg' },
  { id: "theme_crest.s_video_5_bits", title: "Video Blocks 5", type: "static_template", category: "videoblocks", image: '/theme_crest/static/images/web-images/videobanner/video-blocks-4.svg' },

  // Title
  { id: "theme_crest.s_title_1_bits", title: "Title 1", type: "static_template", category: "titles", image: '/theme_crest/static/images/titles/title-text-1.svg' },
  { id: "theme_crest.s_title_2_bits", title: "Title 2", type: "static_template", category: "titles", image: '/theme_crest/static/images/titles/title-text-2.svg' },
  { id: "theme_crest.s_title_3_bits", title: "Title 3", type: "static_template", category: "titles", image: '/theme_crest/static/images/titles/title-text-3.svg' },
  { id: "theme_crest.s_title_4_bits", title: "Title 4", type: "static_template", category: "titles", image: '/theme_crest/static/images/titles/title-text-4.svg' },

  // ABOUT
  { id: "theme_crest.s_about_1", title: "About 1", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-1.svg' },
  { id: "theme_crest.s_about_2", title: "About 2", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-2.svg' },
  { id: "theme_crest.s_about_3", title: "About 3", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-3.svg' },
  { id: "theme_crest.s_about_4", title: "About 4", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-4.svg' },
  { id: "theme_crest.s_about_5", title: "About 5", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-5.svg' },
  { id: "theme_crest.s_about_6", title: "About 6", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-6.svg' },
  { id: "theme_crest.s_about_7", title: "About 7", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-7.svg' },
  { id: "theme_crest.s_about_8", title: "About 8", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-8.svg' },
  { id: "theme_crest.s_about_9", title: "About 9", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-9.svg' },
  { id: "theme_crest.s_about_10", title: "About 10", type: "static_template", category: "about", image: '/theme_crest/static/images/web-images/about/about-10.svg' },

  // Call To Action
  { id: "theme_crest.s_call_to_action_1", title: "Call To Action 1", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-1.svg' },
  { id: "theme_crest.s_call_to_action_2", title: "Call To Action 2", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-2.svg' },
  { id: "theme_crest.s_call_to_action_3", title: "Call To Action 3", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-3.svg' },
  { id: "theme_crest.s_call_to_action_4", title: "Call To Action 4", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-3.svg' },
  { id: "theme_crest.s_call_to_action_5", title: "Call To Action 5", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-4.svg' },
  { id: "theme_crest.s_call_to_action_6", title: "Call To Action 6", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-5.svg' },
  { id: "theme_crest.s_call_to_action_7", title: "Call To Action 7", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-7.svg' },
  { id: "theme_crest.s_call_to_action_8", title: "Call To Action 8", type: "static_template", category: "call_to_action", image: '/theme_crest/static/images/web-images/call-to-aciton/calltoaction-8.svg' },

  // Clients  
  { id: "theme_crest.s_clients_1", title: "Clients 1", type: "static_template", category: "clients", image: '/theme_crest/static/images/web-images/clients/client-section1.svg' },
  { id: "theme_crest.s_clients_2", title: "Clients 2", type: "static_template", category: "clients", image: '/theme_crest/static/images/web-images/clients/client-section-2.svg' },
  { id: "theme_crest.s_clients_3", title: "Clients 3", type: "static_template", category: "clients", image: '/theme_crest/static/images/web-images/clients/client-section-3.svg' },

  // Contact
  { id: "theme_crest.s_contact_1", title: "Contact 1", type: "static_template", category: "contact", image: '/theme_crest/static/images/web-images/contacts/contacts-1.svg' },
  { id: "theme_crest.s_contact_2", title: "Contact 2", type: "static_template", category: "contact", image: '/theme_crest/static/images/web-images/contacts/contacts-2.svg' },
  { id: "theme_crest.s_contact_3", title: "Contact 3", type: "static_template", category: "contact", image: '/theme_crest/static/images/web-images/contacts/contacts-3.svg' },


  // Facts
  { id: "theme_crest.s_facts_1", title: "Facts 1", type: "static_template", category: "facts", image: '/theme_crest/static/images/web-images/facts/fact-1.svg' },
  { id: "theme_crest.s_facts_2", title: "Facts 2", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-2.svg' },
  { id: "theme_crest.s_facts_3", title: "Facts 3", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-3.svg' },
  { id: "theme_crest.s_facts_4", title: "Facts 4", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-4.svg' },
  { id: "theme_crest.s_facts_5", title: "Facts 5", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-5.svg' },
  { id: "theme_crest.s_facts_6", title: "Facts 6", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-6.svg' },
  { id: "theme_crest.s_facts_7", title: "Facts 7", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-7.svg' },
  { id: "theme_crest.s_facts_8", title: "Facts 8", type: "static_template", category: "facts", image: 'theme_crest/static/images/web-images/facts/fact-8.svg' },

  // FAQ

  { id: "theme_crest.s_faq_1", title: "FAQ 1", type: "static_template", category: "faq", image: '/theme_crest/static/images/web-images/faqs/faqs-secs1.svg' },
  { id: "theme_crest.s_faq_2", title: "FAQ 2", type: "static_template", category: "faq", image: '/theme_crest/static/images/web-images/faqs/faqs-secs2.svg' },
  { id: "theme_crest.s_faq_3", title: "FAQ 3", type: "static_template", category: "faq", image: '/theme_crest/static/images/web-images/faqs/faqs-secs3.svg' },

  // Features
  { id: "theme_crest.s_features_1", title: "Features 1", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features1.svg' },
  { id: "theme_crest.s_features_2", title: "Features 2", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features2.svg' },
  { id: "theme_crest.s_features_3", title: "Features 3", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features3.svg' },
  { id: "theme_crest.s_features_4", title: "Features 4", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features4.svg' },
  { id: "theme_crest.s_features_5", title: "Features 5", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features5.svg' },
  { id: "theme_crest.s_features_6", title: "Features 6", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features6.svg' },
  { id: "theme_crest.s_features_7", title: "Features 7", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features7.svg' },
  { id: "theme_crest.s_features_8", title: "Features 8", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features8.svg' },
  { id: "theme_crest.s_features_9", title: "Features 9", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features9.svg' },
  { id: "theme_crest.s_features_10", title: "Features 10", type: "static_template", category: "features", image: '/theme_crest/static/images/web-images/features/features10.svg' },

  // Hero
  { id: "theme_crest.s_hero_1", title: "Hero 1", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero1.svg' },
  { id: "theme_crest.s_hero_2", title: "Hero 2", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero2.svg' },
  { id: "theme_crest.s_hero_3", title: "Hero 3", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero3.svg' },
  { id: "theme_crest.s_hero_4", title: "Hero 4", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero3.svg' },
  { id: "theme_crest.s_hero_5", title: "Hero 5", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero5.svg' },
  { id: "theme_crest.s_hero_6", title: "Hero 6", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero6.svg' },
  { id: "theme_crest.s_hero_7", title: "Hero 7", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero7.svg' },
  { id: "theme_crest.s_hero_8", title: "Hero 8", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero8.svg' },
  { id: "theme_crest.s_hero_9", title: "Hero 9", type: "static_template", category: "hero", image: '/theme_crest/static/images/web-images/hero/hero9.svg' },

  // Portfolio
  { id: "theme_crest.s_portfolio_1", title: "Portfolio 1", type: "static_template", category: "portfolio", image: '/theme_crest/static/images/web-images/portfolio/portfolio-1.svg' },
  { id: "theme_crest.s_portfolio_2", title: "Portfolio 2", type: "static_template", category: "portfolio", image: '/theme_crest/static/images/web-images/portfolio/portfolio-2.svg' },
  { id: "theme_crest.s_portfolio_3", title: "Portfolio 3", type: "static_template", category: "portfolio", image: '/theme_crest/static/images/web-images/portfolio/portfolio-3.svg' },

  // Pricing
  { id: "theme_crest.s_pricing_1", title: "Pricing 1", type: "static_template", category: "pricing", image: '/theme_crest/static/images/svg/block1.svg' },
  { id: "theme_crest.s_pricing_2", title: "Pricing 2", type: "static_template", category: "pricing", image: '/theme_crest/static/images/svg/block1.svg' },
  { id: "theme_crest.s_pricing_3", title: "Pricing 3", type: "static_template", category: "pricing", image: '/theme_crest/static/images/svg/block1.svg' },

  // Process
  { id: "theme_crest.s_process_1", title: "Process 1", type: "static_template", category: "process", image: '/theme_crest/static/images/web-images/process/process-1.svg' },
  { id: "theme_crest.s_process_2", title: "Process 2", type: "static_template", category: "process", image: '/theme_crest/static/images/web-images/process/process-2.svg' },
  { id: "theme_crest.s_process_3", title: "Process 3", type: "static_template", category: "process", image: '/theme_crest/static/images/web-images/process/process-3.svg' },

  // Team
  { id: "theme_crest.s_team_1", title: "Team 1", type: "static_template", category: "team", image: '/theme_crest/static/images/web-images/team/team-1.svg' },
  { id: "theme_crest.s_team_2", title: "Team 2", type: "static_template", category: "team", image: '/theme_crest/static/images/web-images/team/team-2.svg' },
  { id: "theme_crest.s_team_3", title: "Team 3", type: "static_template", category: "team", image: '/theme_crest/static/images/web-images/team/team-3.svg' },
  // Testimonials
  { id: "theme_crest.s_testimonials_1", title: "Testimonials 1", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-1.svg' },
  { id: "theme_crest.s_testimonials_2", title: "Testimonials 2", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-2.svg' },
  { id: "theme_crest.s_testimonials_3", title: "Testimonials 3", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-3.svg' },
  { id: "theme_crest.s_testimonials_4", title: "Testimonials 4", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-4.svg' },
  { id: "theme_crest.s_testimonials_5", title: "Testimonials 5", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-5.svg' },
  { id: "theme_crest.s_testimonials_6", title: "Testimonials 6", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-6.svg' },
  { id: "theme_crest.s_testimonials_7", title: "Testimonials 7", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-7.svg' },
  { id: "theme_crest.s_testimonials_8", title: "Testimonials 8", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-8.svg' },
  { id: "theme_crest.s_testimonials_9", title: "Testimonials 9", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-9.svg' },
  { id: "theme_crest.s_testimonials_10", title: "Testimonials 10", type: "static_template", category: "testimonials", image: '/theme_crest/static/images/web-images/testimonial/testimonial-10.svg' },

];

export const DOMAIN_TEMPLATE = {
  name: {
    displayName: "Name",
    operators: [
      {
        name: "contains",
        operator: "ilike",
        value: "string",
      },
      {
        name: "doesnot contain",
        operator: "not ilike",
        value: "string",
      },
      {
        name: "is equal to",
        operator: "=",
        value: "string",
      },
      {
        name: "is not equal to",
        operator: "!=",
        value: "string",
      },
    ],
  },
  public_categ_ids: {
    displayName: "categories",
    operators: [
      {
        name: "is in",
        operator: "in",
        type: "array",
      },
      {
        name: "is not in",
        operator: "not in",
        type: "array",
      },
    ],
  },
  list_price: {
    displayName: "Price",
    operators: [
      {
        name: "equal to",
        operator: "=",
        type: "number",
      },
      {
        name: "not equal to",
        operator: "!=",
        type: "number",
      },
      {
        name: "Greater than",
        operator: ">",
        type: "number",
      },
      {
        name: "less than",
        operator: "<",
        type: "number",
      },
      {
        name: "less than or equal to",
        operator: "<=",
        type: "number",
      },
      {
        name: "greater than or equal to",
        operator: ">=",
        type: "number",
      },
    ],
  },
};
