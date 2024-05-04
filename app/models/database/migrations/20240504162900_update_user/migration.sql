/*
  Warnings:

  - You are about to drop the column `acreage` on the `Assets` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[tokenId]` on the table `Assets` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `isMine` to the `Assets` table without a default value. This is not possible if the table is not empty.
  - Added the required column `price` to the `Assets` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Assets" DROP COLUMN "acreage",
ADD COLUMN     "isMine" BOOLEAN NOT NULL,
ADD COLUMN     "price" DOUBLE PRECISION NOT NULL,
ADD COLUMN     "tokenId" TEXT;

-- CreateIndex
CREATE UNIQUE INDEX "Assets_tokenId_key" ON "Assets"("tokenId");
