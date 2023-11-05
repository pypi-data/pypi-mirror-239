/*
 * Copyright 2022 Jussi Pakkanen
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define _USE_MATH_DEFINES
#include <pdfgen.hpp>
#include <cmath>

using namespace capypdf;

namespace {

constexpr double mm2pt(const double x) { return x * 2.8346456693; }

const double page_w = mm2pt(130);
const double page_h = mm2pt(210);
const double spine_w = mm2pt(20);
const double bleed = mm2pt(10);
const double margin = mm2pt(20);

const double paper_height = page_h + 2 * margin;
const double paper_width = 2 * (margin + page_w) + spine_w;

void draw_registration_cross(PdfDrawContext &ctx, double x, double y, const double cross_size) {
    const double circle_size = 0.6 * cross_size;
    ctx.cmd_q();
    ctx.translate(x, y);
    ctx.cmd_m(-cross_size / 2, 0);
    ctx.cmd_l(cross_size / 2, 0);
    ctx.cmd_m(0, -cross_size / 2);
    ctx.cmd_l(0, cross_size / 2);
    ctx.cmd_S();
    ctx.cmd_w(1 / circle_size);
    ctx.scale(circle_size, circle_size);
    ctx.draw_unit_circle();
    ctx.cmd_S();
    ctx.cmd_Q();
}

void draw_colorbox(PdfDrawContext &ctx,
                   double box_size,
                   double xloc,
                   double yloc,
                   double c,
                   double m,
                   double y,
                   double k) {
    ctx.cmd_q();
    ctx.translate(xloc, yloc);
    ctx.scale(box_size, box_size);
    ctx.cmd_k(c, m, y, k);
    ctx.draw_unit_box();
    ctx.cmd_f();
    ctx.cmd_Q();
}

void draw_colorbar(PdfDrawContext &ctx) {
    const double box_size = mm2pt(5);
    const double yloc = (margin - bleed) / 2;
    draw_colorbox(ctx, box_size, 2 * margin, yloc, 1.0, 0.0, 0.0, 0.0);
    draw_colorbox(ctx, box_size, 2 * margin + box_size, yloc, 0.0, 1.0, 0.0, 0.0);
    draw_colorbox(ctx, box_size, 2 * margin + 2 * box_size, yloc, 0.0, 0.0, 1.0, 0.0);
    draw_colorbox(ctx, box_size, 2 * margin + 3 * box_size, yloc, 1.0, 1.0, 0.0, 0.0);
    draw_colorbox(ctx, box_size, 2 * margin + 4 * box_size, yloc, 1.0, 0.0, 1.0, 0.0);
    draw_colorbox(ctx, box_size, 2 * margin + 5 * box_size, yloc, 0.0, 1.0, 1.0, 0.0);
}

void draw_graybar(PdfDrawContext &ctx) {
    const double box_size = mm2pt(5);
    const double xloc = paper_width / 2 + margin;
    const double yloc = paper_height - (margin - bleed) / 2;
    for(int i = 1; i < 11; ++i) {
        draw_colorbox(ctx, box_size, xloc + i * box_size, yloc, 0.0, 0.0, 0.0, i / 10.0);
    }
}

void draw_registration_marks(PdfDrawContext &ctx) {
    const double cross_size = mm2pt(10); // diameter, not radius
    draw_registration_cross(ctx, cross_size / 2, paper_height / 2, cross_size);
    draw_registration_cross(ctx, paper_width - cross_size / 2, paper_height / 2, cross_size);
    draw_registration_cross(ctx, paper_width / 2, cross_size / 2, cross_size);
    draw_registration_cross(ctx, paper_width / 2, paper_height - cross_size / 2, cross_size);
}

void draw_trim_marks(PdfDrawContext &ctx) {
    const auto len = margin / 2;
    ctx.cmd_m(margin, 0);
    ctx.cmd_l(margin, len);
    ctx.cmd_m(0, margin);
    ctx.cmd_l(len, margin);

    ctx.cmd_m(0, paper_height - margin);
    ctx.cmd_l(len, paper_height - margin);
    ctx.cmd_m(margin, paper_height);
    ctx.cmd_l(margin, paper_height - len);

    ctx.cmd_m(paper_width, paper_height - margin);
    ctx.cmd_l(paper_width - len, paper_height - margin);
    ctx.cmd_m(paper_width - margin, paper_height);
    ctx.cmd_l(paper_width - margin, paper_height - len);

    ctx.cmd_m(paper_width - margin, 0);
    ctx.cmd_l(paper_width - margin, len);
    ctx.cmd_m(paper_width - 0, margin);
    ctx.cmd_l(paper_width - len, margin);

    ctx.cmd_S();
}

} // namespace

int main(int, char **) {
    PdfGenerationData opts;

    opts.default_page_properties.mediabox->x1 = opts.default_page_properties.mediabox->y1 = 0;
    opts.default_page_properties.mediabox->x2 = paper_width;
    opts.default_page_properties.mediabox->y2 = paper_height;

    opts.default_page_properties.trimbox =
        PdfRectangle{margin, margin, paper_width - 2 * margin, paper_height - 2 * margin};
    opts.title = u8string::from_cstr("Book cover generation experiment with utf-8 (ö).").value();
    opts.author = u8string::from_cstr("G. R. Aphicdesigner").value();
    opts.output_colorspace = CAPYPDF_CS_DEVICE_CMYK;
    opts.prof.cmyk_profile_file =
        "/home/jpakkane/Downloads/temp/Adobe ICC Profiles (end-user)/CMYK/UncoatedFOGRA29.icc";

    try {
        GenPopper genpop("cover.pdf", opts);
        PdfGen &gen = *genpop.g;
        auto image_id = gen.load_image("gradient.png").value();
        auto sep_id = gen.create_separation("Gold", DeviceCMYKColor{0, 0.03, 0.55, 0.08});
        {
            auto ctxguard = gen.guarded_page_context();
            auto &ctx = ctxguard.ctx;
            ctx.cmd_w(1.0);
            ctx.set_nonstroke_color(DeviceRGBColor{0.9, 0.9, 0.9});
            ctx.cmd_re(margin - bleed,
                       margin - bleed,
                       opts.default_page_properties.mediabox->x2 - 2 * (margin - bleed),
                       opts.default_page_properties.mediabox->y2 - 2 * (margin - bleed));
            ctx.cmd_f();
            ctx.set_nonstroke_color(DeviceRGBColor{0.9, 0.2, 0.2});
            ctx.cmd_re(margin,
                       margin,
                       opts.default_page_properties.mediabox->x2 - 2 * (margin),
                       opts.default_page_properties.mediabox->y2 - 2 * (margin));
            ctx.cmd_f();
            ctx.set_nonstroke_color(DeviceRGBColor{0.2, 0.9, 0.2});
            ctx.cmd_re(paper_width / 2 - spine_w / 2, margin, spine_w, page_h);
            ctx.cmd_f();
            ctx.set_nonstroke_color(DeviceRGBColor{0, 0, 0});
            {
                auto pop = ctx.push_gstate();
                ctx.translate((paper_width + spine_w + page_w - 100) / 2, paper_height / 2 - 100);
                ctx.scale(100, 100);
                ctx.draw_image(image_id);
            }
            ctx.set_color(SeparationColor{sep_id, 1.0}, false);
            ctx.render_pdfdoc_text_builtin("Front Cover",
                                           CAPY_FONT_HELVETICA_BOLD,
                                           48,
                                           paper_width / 2 + page_w / 5,
                                           2 * paper_height / 3);
            ctx.set_nonstroke_color(DeviceRGBColor{1.0, 1.0, 1.0});
            ctx.render_pdfdoc_text_builtin("Lorem ipsum dolor sit amet,",
                                           CAPY_FONT_TIMES_ROMAN,
                                           12,
                                           margin + page_w / 6,
                                           2 * paper_height / 3);
            ctx.render_pdfdoc_text_builtin("consectetur adipiscing elit",
                                           CAPY_FONT_TIMES_ROMAN,
                                           12,
                                           margin + page_w / 6,
                                           2 * paper_height / 3 - 12);
            {
                auto pop = ctx.push_gstate();
                ctx.set_nonstroke_color(DeviceRGBColor{0.0, 0.0, 0.0});
                ctx.translate(paper_width / 2, 3 * paper_height / 4);
                ctx.rotate(-M_PI / 2.0);
                ctx.render_pdfdoc_text_builtin("Name of Book", CAPY_FONT_HELVETICA_BOLD, 12, 0, 0);
                // ctx.cmd_re(0, 0, 10, 10);
                ctx.cmd_f();
            }
            ctx.set_nonstroke_color(DeviceGrayColor{0});
            ctx.render_pdfdoc_text_builtin("PDF created: YYYY-MM-DD HH:MM",
                                           CAPY_FONT_TIMES_ROMAN,
                                           10,
                                           paper_width / 2 + page_w / 5,
                                           10);
            draw_colorbar(ctx);
            draw_graybar(ctx);
            ctx.set_all_stroke_color();
            draw_registration_marks(ctx);
            draw_trim_marks(ctx);
        }

    } catch(const std::exception &e) {
        printf("ERROR: %s\n", e.what());
        return 1;
    }

    return 0;
}
