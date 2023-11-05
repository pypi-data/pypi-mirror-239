/*
 * Copyright 2023 Jussi Pakkanen
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

#include <pdfgen.hpp>

using namespace capypdf;

static void draw_intersect_shape(PdfDrawContext &ctx) {
    ctx.cmd_m(50, 90);
    ctx.cmd_l(80, 10);
    ctx.cmd_l(10, 60);
    ctx.cmd_l(90, 60);
    ctx.cmd_l(20, 10);
    ctx.cmd_h();
}

void basic_painting(PdfDrawContext &ctx) {
    ctx.cmd_w(5);
    {
        auto pop = ctx.push_gstate();
        ctx.cmd_J(CAPY_LC_ROUND);
        ctx.cmd_m(10, 10);
        ctx.cmd_c(80, 10, 20, 90, 90, 90);
        ctx.cmd_S();
    }
    {
        auto pop = ctx.push_gstate();
        ctx.cmd_w(10);
        ctx.translate(100, 0);
        ctx.set_stroke_color(DeviceRGBColor{1.0, 0.0, 0.0});
        ctx.set_nonstroke_color(DeviceRGBColor{0.9, 0.9, 0.0});
        ctx.cmd_j(CAPY_LJ_BEVEL);
        ctx.cmd_m(50, 90);
        ctx.cmd_l(10, 10);
        ctx.cmd_l(90, 10);
        ctx.cmd_h();
        ctx.cmd_B();
    }
    {
        auto pop = ctx.push_gstate();
        ctx.translate(0, 100);
        draw_intersect_shape(ctx);
        ctx.cmd_w(3);
        ctx.set_nonstroke_color(DeviceRGBColor{0, 1, 0});
        ctx.set_stroke_color(DeviceRGBColor{0.5, 0.1, 0.5});
        ctx.cmd_j(CAPY_LJ_ROUND);
        ctx.cmd_B();
    }
    {
        auto pop = ctx.push_gstate();
        ctx.translate(100, 100);
        ctx.cmd_w(2);
        ctx.set_nonstroke_color(DeviceRGBColor{0, 1, 0});
        ctx.set_stroke_color(DeviceRGBColor{0.5, 0.1, 0.5});
        draw_intersect_shape(ctx);
        ctx.cmd_Bstar();
    }
}

void clipping(PdfDrawContext &ctx, CapyPDF_ImageId image) {
    ctx.cmd_w(0.1);
    {
        auto pop = ctx.push_gstate();

        draw_intersect_shape(ctx);
        ctx.cmd_Wstar();
        ctx.cmd_n();
        ctx.scale(100, 100);
        ctx.draw_image(image);
    }
    {
        auto pop = ctx.push_gstate();
        ctx.translate(100, 0);
        ctx.cmd_Tr(CAPY_TEXT_CLIP);
        ctx.render_pdfdoc_text_builtin("Awesome!", CAPY_FONT_TIMES_ROMAN, 18, 10, 50);
        ctx.scale(100, 100);
        ctx.draw_image(image);
    }
}

int main(int argc, char **argv) {
    PdfGenerationData opts;

    const char *image = argc > 1 ? argv[1] : "../pdfgen/images/flame_gradient.png";
    opts.default_page_properties.mediabox->x2 = opts.default_page_properties.mediabox->y2 = 200;
    opts.title = u8string::from_cstr("PDF path test").value();
    opts.author = u8string::from_cstr("Test Person").value();
    opts.output_colorspace = CAPYPDF_CS_DEVICE_RGB;
    {
        GenPopper genpop("path_test.pdf", opts);
        PdfGen &gen = *genpop.g;
        auto ctxp = gen.guarded_page_context();
        auto &ctx = ctxp.ctx;
        basic_painting(ctx);
        gen.add_page(ctx);
        auto bg_img = gen.load_image(image).value();
        clipping(ctx, bg_img);
    }
    return 0;
}
